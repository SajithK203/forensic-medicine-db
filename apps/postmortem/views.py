from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Postmortem
from .forms  import PostmortemForm
from apps.core.decorators import doctor_or_admin
from apps.core.middleware  import log_action

@login_required
def pm_list(request):
    qs = Postmortem.objects.select_related('case','doctor').all()
    death_type = request.GET.get('death_type','')
    if death_type: qs = qs.filter(death_type=death_type)
    paginator = Paginator(qs, 20)
    return render(request, 'postmortem/list.html', {
        'page_obj': paginator.get_page(request.GET.get('page')),
        'death_type': death_type, 'page_title': 'Postmortem Records', 'active_nav': 'postmortem'})

@login_required
@doctor_or_admin
def pm_create(request):
    form = PostmortemForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        pm = form.save()
        log_action(request.user,'CREATE','Postmortem',pm.postmortem_id,'',request)
        messages.success(request, f'Postmortem {pm.postmortem_id} recorded.')
        return redirect('cases:detail', pk=pm.case.case_id)
    return render(request, 'postmortem/form.html', {
        'form': form, 'action': 'Record Postmortem',
        'page_title': 'New Postmortem', 'active_nav': 'postmortem'})

@login_required
@doctor_or_admin
def pm_edit(request, pk):
    pm   = get_object_or_404(Postmortem, pk=pk)
    form = PostmortemForm(request.POST or None, instance=pm)
    if request.method == 'POST' and form.is_valid():
        form.save()
        log_action(request.user,'UPDATE','Postmortem',pk,'',request)
        messages.success(request, 'Postmortem updated.')
        return redirect('cases:detail', pk=pm.case.case_id)
    return render(request, 'postmortem/form.html', {
        'form': form, 'pm': pm, 'action': 'Edit Postmortem',
        'page_title': f'Edit {pk}', 'active_nav': 'postmortem'})
