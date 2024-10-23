from django.shortcuts import render, get_object_or_404, redirect
from store.models import Product
from .models import Cart, CartItem, Order, OrderItem, Coupon
from django.contrib import messages
from django.db.models import F, ExpressionWrapper, When, Case, DecimalField, FloatField
from django.db.models.functions import Coalesce
from django.db.models import Sum, fields
from user.models import Address
from .forms import NewCheckoutAddressForm
from django.views import View
from django.http import HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.core.exceptions import ObjectDoesNotExist


class CartSummaryMixin:
    template_name = "cart/cart-summary.html"

    def get_context_data(self, **kwargs):
        if not self.request.user.is_authenticated:
            return
        else:
            exclude_out_of_stock = kwargs.pop(
                "exclude_out_of_stock", False
            )  # Extracting the flag from kwargs
            cart = Cart.objects.get_or_create(user=self.request.user)[0]

            # Getting cart items with total prices annotated
            cart_items = CartItem.objects.filter(cart=cart)

            #  Excluding out-of-stock items if specified
            if exclude_out_of_stock:
                cart_items = cart_items.exclude(product__current_stock=0)

            # Annotating the maximum discount for each cart item
            cart_items = cart_items.annotate(
                max_discount=Case(
                    When(
                        product__category__categoryoffers__discount_percentage__gt=Coalesce(
                            F("product__productoffers__discount_percentage"), 0
                        ),
                        then=F(
                            "product__category__categoryoffers__discount_percentage"
                        ),
                    ),
                    default=F("product__productoffers__discount_percentage"),
                    output_field=FloatField(),
                )
            )

            # Calculating total price before discounts
            total_price_before_discount = ExpressionWrapper(
                F("quantity") * F("product__price"), output_field=FloatField()
            )

            # Calculating total price after applying the maximum discount
            total_price_after_discount = ExpressionWrapper(
                F("quantity")
                * F("product__price")
                * Coalesce((1 - (float("0.01") * F("max_discount"))), 1),
                output_field=FloatField(),
            )

            # Annotating total prices before and after discounts to cart items
            cart_items = cart_items.annotate(
                total_price_before_discount=total_price_before_discount,
                total_price_after_discount=total_price_after_discount,
            )

            # Calculating the grand total before discount
            grand_total_before_discount = (
                cart_items.exclude(product__current_stock=0).aggregate(
                    grand_total_before_discount=Sum("total_price_before_discount")
                )["grand_total_before_discount"]
                or 0
            )

            # Calculating the grand total after discount
            grand_total_after_discount = (
                cart_items.exclude(product__current_stock=0).aggregate(
                    grand_total=Sum("total_price_after_discount")
                )["grand_total"]
                or 0
            )

            # Calculatin the total promotional discount applied
            total_promotional_discount = (
                grand_total_before_discount - grand_total_after_discount
            )

            # Adjusting the grand total if a coupon is applied
            if cart.coupon:
                grand_total_after_discount -= cart.coupon.discount_price

            # Creating the context dictionary
            context = {
                "cart_items": cart_items,
                "grand_total": grand_total_after_discount,
                "total_promotional_discount": total_promotional_discount,
                "grand_total_before_discount": grand_total_before_discount,
            }

            context.update(kwargs)
            return context


# To show the cart detailed view before checkout
class CartSummaryView(CartSummaryMixin, View):
    def get(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect("login")
        else:
            return render(request, self.template_name, self.get_context_data())


# To add item to the cart from the product-info html
def cart_add(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    quantity = int(request.POST.get("quantity"))
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

    if quantity > 10:
        messages.warning(
            request, "The maximum quantity allowed is 10. Item not added to the cart."
        )
    else:
        if not created:
            messages.warning(request, "The Products exist in the cart")
        else:
            cart_item.quantity = quantity
            cart_item.save()
            messages.success(request, "The item has been added to the cart")
    return redirect(request.META["HTTP_REFERER"])


# checks whether the total satisfies the minimum amount required for a coupon before deleting


class DeleteCartItem(CartSummaryMixin, View):
    def get(self, request, pk, *args, **kwargs):
        user_cart = request.user.cart.first()
        cart_summary_context = self.get_context_data(exclude_out_of_stock=True)
        grand_total = cart_summary_context["grand_total"]

        # deleting the item from the cart which the user requested for
        instance = CartItem.objects.get(pk=pk)
        instance.delete()

        # getting the context for the summary page after the quantity has been updated
        cart_summary_context = self.get_context_data(exclude_out_of_stock=True)
        grand_total = cart_summary_context["grand_total"]

        # checks whether the new grand total meets the minimum amount of the coupon
        if user_cart.coupon:
            coupon_amount = user_cart.coupon.discount_price
            minimum_amount = user_cart.coupon.minimum_amount

            if grand_total + coupon_amount < minimum_amount:
                user_cart.coupon = None

                user_cart.save()
                messages.info(
                    request,
                    f"The Minimum amount required to apply this coupon is {minimum_amount}. Coupon has been remove",
                    extra_tags="info-danger",
                )

        return redirect(request.META["HTTP_REFERER"])


# view to update the quantity in the cart
# checks whether the total satisfies the minimum amount required for a coupon before updating


class UpdateCheckoutView(CartSummaryMixin, View):
    def post(self, request, pk, *args, **kwargs):
        user_cart = request.user.cart.first()
        updated_quantity_key = f"quantity_{pk}"
        updated_quantity = int(request.POST.get(updated_quantity_key))

        # updating the quantity as entered by the user
        cart_item = CartItem.objects.get(pk=pk)
        cart_item.quantity = updated_quantity
        cart_item.save()

        # getting the context for the summary page after the quantity has been updated
        cart_summary_context = self.get_context_data(exclude_out_of_stock=True)
        grand_total = cart_summary_context["grand_total"]

        # checks whether the new grand total meets the minimum amount of the coupon
        if user_cart.coupon:
            coupon_amount = user_cart.coupon.discount_price
            minimum_amount = user_cart.coupon.minimum_amount

            if grand_total + coupon_amount < minimum_amount:
                user_cart.coupon = None

                user_cart.save()
                messages.info(
                    request,
                    f"The Minimum amount required to apply this coupon is {minimum_amount}. Coupon has been remove",
                    extra_tags="info-danger",
                )

        return render(
            request, "cart/cart-summary-partial.html", self.get_context_data()
        )


# Views for various forms in the checkout page


class CheckoutView(CartSummaryMixin, View):
    template_name = "cart/checkout.html"

    def get(self, request, *args, **kwargs):

        user_cart = request.user.cart.all()
        cart_summary_context = self.get_context_data(exclude_out_of_stock=True)
        grand_total = cart_summary_context["grand_total"]

        if user_cart.first().coupon:
            minimum_amount = user_cart[0].coupon.minimum_amount

            if grand_total < minimum_amount:
                messages.warning(
                    request,
                    f"The Minimum amount required to apply this coupon is {minimum_amount}",
                )
                return HttpResponseRedirect(request.META.get("HTTP_REFERER"))

        try:
            default_address = Address.objects.get(
                user=request.user, default_address=True
            )
        except ObjectDoesNotExist:
            default_address = None

        try:
            other_addresses = Address.objects.filter(
                user=request.user, default_address=False
            )
        except ObjectDoesNotExist:
            other_addresses = None

        form = NewCheckoutAddressForm()

        # Before proceeding to the checkout checking whether the quantity matches with the inventory
        inventory_status = self.check_inventory_status()
        if inventory_status["status"] == "error":
            messages.warning(request, inventory_status["message"])
            return redirect("cart-summary")

        # Getting the cart items and store them in the session to display the same content in the checkout
        cart_items = cart_summary_context["cart_items"]
        request.session["cart_items_for_checkout"] = list(
            cart_items.values_list("id", flat=True)
        )
        cart = Cart.objects.filter(user=request.user).first()

        if cart.coupon:
            request.session["coupon_discount"] = cart.coupon.discount_price

        context = {
            "default_address": default_address,
            "other_addresses": other_addresses,
            "form": form,
            **cart_summary_context,
        }

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        selected_address_type = request.POST.get("selected_address_type")
        selected_payment_method = request.POST.get("selected_payment_method")
        payment_status = request.POST.get("payment_status")
        user = request.user

        if selected_address_type == "new":
            form = NewCheckoutAddressForm(request.POST)
            if form.is_valid():
                address_instance = form.save(commit=False)
                address_instance.user = user
                address_instance.save()
                shipping_address = address_instance
        else:
            address_id = request.POST.get("address_id")
            shipping_address = Address.objects.get(id=address_id)

        if selected_payment_method == "paypal":
            payment_method = "PayPal"
        else:
            payment_method = "COD"

        # Retrieve the stored cart items from the session
        cart_items_ids = request.session.pop("cart_items_for_checkout", [])
        cart_items = CartItem.objects.filter(id__in=cart_items_ids)
        if "coupon_discount" in request.session:
            coupon_discount = request.session["coupon_discount"]
        else:
            coupon_discount = 0

        order = self.create_order(
            coupon_discount, user, shipping_address, payment_method, payment_status
        )

        # Moving cart items to the order
        for cart_item in cart_items:

            discounted_price = cart_item.product.get_discounted_price()
            discount = discounted_price

            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                qty=cart_item.quantity,
                price=cart_item.product.price,
                discount=discount,
            )

            # Update product quantity in the inventory
            cart_item.product.current_stock -= cart_item.quantity
            cart_item.product.save()

        # Removing cart items from the cart
        cart_items.delete()

        return redirect("success-page")

    def create_order(
        self, coupon_discount, user, shipping_address, payment_method, payment_status
    ):
        return Order.objects.create(
            shipping_address=shipping_address,
            payment_method=payment_method,
            user=user,
            coupon_discount=coupon_discount,
            payment_status=payment_status,
        )

    def check_inventory_status(self):
        cart_summary_context = self.get_context_data(exclude_out_of_stock=True)
        cart_items = cart_summary_context["cart_items"]

        for cart_item in cart_items:
            if cart_item.product.current_stock < cart_item.quantity:
                return {
                    "status": "error",
                    "message": f"Sorry, {cart_item.product.title} is low in stock. You can order up to {cart_item.product.current_stock} units.",
                }

        return {"status": "success"}


# Views related to coupon management


class CouponView(CartSummaryMixin, View):

    template_name = (
        "cart/cart-summary-partial.html"  # Template containing the updated cart summary
    )

    def post(self, request):
        cart_obj = Cart.objects.get(user=request.user)
        coupon_code = request.POST.get("coupon")
        coupon_obj = Coupon.objects.filter(coupon_code__icontains=coupon_code).first()
        cart_summary_context = self.get_context_data(exclude_out_of_stock=True)

        if not coupon_obj:
            messages.info(request, "Invalid Coupon", extra_tags="info-danger")
        elif cart_obj.coupon:
            messages.info(request, "Coupon already applied", extra_tags="info-danger")
        elif coupon_obj.is_expired:
            messages.info(request, "Coupon Expired", extra_tags="info-danger")

        else:
            grand_total = cart_summary_context["grand_total"]
            minimum_amount = coupon_obj.minimum_amount

            if grand_total < minimum_amount:
                messages.info(
                    request,
                    f"Amount should be greater than {minimum_amount}",
                    extra_tags="info-danger",
                )
            else:
                cart_obj.coupon = coupon_obj
                cart_obj.save()
                cart_summary_context = self.get_context_data(exclude_out_of_stock=True)
                messages.info(
                    request,
                    "Coupon has been succesfully applied",
                    extra_tags="info-success",
                )

                return render(
                    request, "cart/cart-summary-partial.html", cart_summary_context
                )

        # Return error message in JSON response
        return render(request, "cart/cart-summary-partial.html", cart_summary_context)

    def delete(self, request, *args, **kwargs):
        user = request.user
        cart = Cart.objects.filter(user=user).first()
        cart.coupon = None
        cart.save()
        messages.info(request, "Coupon Removed.", extra_tags="info-success")
        cart_summary_context = self.get_context_data(exclude_out_of_stock=True)
        return render(request, "cart/cart-summary-partial.html", cart_summary_context)


def success_page(request):

    order_instance = Order.objects.filter(user=request.user).last()

    order_items = OrderItem.objects.filter(order=order_instance).annotate(
        total_price=ExpressionWrapper(
            F("qty") * F("price"),
            output_field=fields.DecimalField(max_digits=10, decimal_places=2),
        ),
        total_discount=ExpressionWrapper(
            F("qty") * F("discount"),
            output_field=fields.DecimalField(max_digits=10, decimal_places=2),
        ),
    )

    total_order_amount_before_discount = (
        order_items.aggregate(total_order_amount_before_discount=Sum("total_price"))[
            "total_order_amount_before_discount"
        ]
        or 0
    )

    total_order_discount = abs(
        order_items.aggregate(total_order_discount=Sum("total_discount"))[
            "total_order_discount"
        ]
        or 0
    )

    coupon_discount = order_instance.coupon_discount

    total_order_amount_after_all_discount = (
        total_order_amount_before_discount - total_order_discount - coupon_discount
    )

    context = {
        "total_order_amount_before_discount": total_order_amount_before_discount,
        "total_order_discount": total_order_discount,
        "total_order_amount_after_all_discount": total_order_amount_after_all_discount,
        "coupon_discount": coupon_discount,
        "order_items": order_items,
        "order_instance": order_instance,
    }

    return render(request, "cart/success-page.html", context)
