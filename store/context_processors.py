def cart_count(request):
    cart = request.session.get('cart', {})
    return {'cart_count': sum(v['quantity'] for v in cart.values())}
