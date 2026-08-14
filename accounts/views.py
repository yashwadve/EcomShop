from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .forms import SignUpForm, UserUpdateForm, UserProfileForm, AddressForm
from .models import UserProfile, Address


def register_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.create(user=user)
            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'accounts/register.html', {'form': form})


@login_required
def profile_view(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, instance=profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('accounts:my_profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = UserProfileForm(instance=profile)

    return render(request, 'accounts/profile.html', {
        'user_form': user_form,
        'profile_form': profile_form,
    })


@login_required
def addresses_view(request):
    """Single page: lists all addresses + handles the 'Add Address' form.
    Edit is done via modal (same list page, populated via JS) posting to edit_address_view.
    """
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    addresses = profile.addresses.all()

    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.user_profile = profile

            if address.is_default:
                profile.addresses.update(is_default=False)

            address.save()
            messages.success(request, 'Address added successfully!')
            return redirect('accounts:my_addresses')
    else:
        form = AddressForm()

    return render(request, 'accounts/addresses.html', {
        'addresses': addresses,
        'form': form,
    })


@login_required
def edit_address_view(request, address_id):
    """Handles the edit modal submission. Redirects back to the addresses list either way."""
    address = get_object_or_404(Address, id=address_id, user_profile__user=request.user)

    if request.method == 'POST':
        form = AddressForm(request.POST, instance=address)
        if form.is_valid():
            updated_address = form.save(commit=False)

            if updated_address.is_default:
                address.user_profile.addresses.exclude(id=address.id).update(is_default=False)

            updated_address.save()
            messages.success(request, 'Address updated successfully!')
        else:
            messages.error(request, 'Please correct the errors and try again.')
        return redirect('accounts:my_addresses')

    # GET request: used to fetch this address's data to prefill the edit modal via JS
    return JsonResponse({
        'id': address.id,
        'full_name': address.full_name,
        'phone': address.phone,
        'address_line1': address.address_line1,
        'address_line2': address.address_line2 or '',
        'city': address.city,
        'state': address.state,
        'pincode': address.pincode,
        'is_default': address.is_default,
    })


@login_required
@require_POST
def delete_address_view(request, address_id):
    """POST-only, no confirm page — confirmation handled by JS (confirm() dialog) in the template."""
    address = get_object_or_404(Address, id=address_id, user_profile__user=request.user)
    address.delete()
    messages.success(request, 'Address deleted.')
    return redirect('accounts:my_addresses')


