from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import discountCode
from .forms import discountForms
# Create your views here.

@login_required
def discount_apply(request):
	now = timezone.now()
	form = discountForms()
	if form.is_valid():
		code = form.cleaned_data['code']
		try:
			discount = discountCode.objects.get(code_iexact=code,valid_from_lte=now,valid_to_gte=now,active=True)
			request.session['discount_id'] = discount_id
		except discountCode.DoesNotExist:
			request.session['discount_id'] = None
	return redirect('cart:cart_details')