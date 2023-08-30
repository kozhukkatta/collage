from django.urls import path,include
from. import views

urlpatterns = [
    path('',views.home,name='home'),
    path('signin',views.signin,name='signin'),
    path('signup',views.signup,name='signup'),
    path('course',views.course,name='course'),
    path('adminhome',views.adminhome,name='adminhome'),
    path('teacherhome',views.teacherhome,name='teacherhome'),
    path('addstudent',views.addstudent,name='addstudent'),
    path('log',views.log,name='log'),
    path('add_course',views.add_course,name='add_course'),
    path('add_student',views.add_student,name='add_student'),
    path('add_teacher',views.add_teacher,name='add_teacher'),
    path('student_det',views.student_det,name='student_det'),
    path('teacher_det',views.teacher_det,name='teacher_det'),
    path('delete_teacher/<int:pk>',views.delete_teacher,name='delete_teacher'),
    path('delete_student/<int:pk>',views.delete_student,name='delete_student'),
    path('edit_student/<int:pk>',views.edit_student,name='edit_student'),
    path('edit_stu/<int:pk>',views.edit_stu,name='edit_stu'),
    path('tedit',views.tedit,name='tedit'),
    path('profile',views.profile,name='profile'),


    path('logout',views.logout,name='logout'),

]