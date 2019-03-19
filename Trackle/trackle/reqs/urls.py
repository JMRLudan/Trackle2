from django.urls import include, path

from .views import pisay, students, teachers

urlpatterns = [
    path('', pisay.home, name='home'),

    path('students/', include(([
        path('', students.RequirementListView.as_view(), name='requirement_list'),
        path('subjects/', students.StudentSubjectsView.as_view(), name='student_subjects'),
        path('finished/', students.TakenRequirementListView.as_view(), name='finished_requirement_list'),
        path('requirement/<int:pk>/', students.RequirementView.as_view(), name='requirement_details'),
        path('requirement/<int:pk>/comment/', students.AddCommentView.as_view(), name='comment_add'),
    ], 'classroom'), namespace='students')),

    path('teachers/', include(([
        path('', teachers.RequirementListView.as_view(), name='req_change_list'),
        path('subjects/add/', teachers.SubjectCreateView.as_view(), name='sub_add'),
        path('requirement/add/', teachers.RequirementCreateView.as_view(), name='req_add'),
        path('requirement/<int:pk>/', teachers.RequirementUpdateView.as_view(), name='requirement_change'),
        path('requirement/<int:pk>/delete/', teachers.RequirementDeleteView.as_view(), name='requirement_delete'),
        path('requirement/<int:pk>/comment/', teachers.AddCommentView.as_view(), name='comment_add'),
    ], 'classroom'), namespace='teachers')),
]
