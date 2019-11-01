from django.urls import path, include

from classroom import views

app_name = 'classroom'

course_patterns = [
    path(
        '',
        views.CourseListCreateAPIView.as_view(),
        name='course-list'
    ),
    path(
        '<int:course_pk>/',
        views.CourseDetailAPIView.as_view(),
        name='course-detail'
    ),
]

lecture_patterns = [
    path(
        '',
        views.LectureListCreateAPIView.as_view(),
        name='lecture-list'
    ),
    path(
        '<int:lecture_pk>/',
        views.LectureDetailAPIView.as_view(),
        name='lecture-detail'
    ),
]

member_patterns = [
    path(
        '', 
        views.CourseMembersListCreateAPIView.as_view(),
        name='course-members-list'
    ),
    path(
        '<str:username>/',  
        views.CourseMembersDestroyAPIView.as_view(),
        name='course-members-remove'
    ),
]

problem_patterns = [
    path(
        '',
        views.UserProblemListAPIView.as_view(),
        name='user-problem-list'
    ),
    path(
        '<int:problem_pk>/',
        views.UserProblemDetailAPIView.as_view(),
        name='user-problem-detail'
    ),
    path(
        '<int:problem_pk>/solution/',
        views.UserProblemSolutionAPIView.as_view(),
        name='problem-solution'
    ),
    path(
        '<int:problem_pk>/comments/',
        views.CommentListCreateAPIView.as_view(),
        name='comment-list'
    ),
]

homework_patterns = [
    path(
        'problems/',
        views.ProblemListCreateAPIView.as_view(),
        name='problem-list'
    ),
    path(
        'done-problems/',
        views.DoneProblemListAPIView.as_view(),
        name='done-problem-list'
    ),
    path(
        'done-problems/<int:problem_pk>/',
        views.DoneProblemRetriveAPIView.as_view(),
        name='done-problem-list'
    ),
    path(
        'done-problems/<int:problem_pk>/mark/',
        views.DoneProblemMarkUpdateAPIView.as_view(),
        name='done-problem-list'
    ),
    path(
        'done-problems/<int:problem_pk>/comments/',
        views.CommentListCreateAPIView.as_view(),
        name='done-problem-comment'
    )
]

urlpatterns = [
    path(
        'courses/',
        include(course_patterns),   
    ),
    path(
        'courses/<int:course_pk>/members/',
        include(member_patterns)
    ),
    path(
        'courses/<int:course_pk>/lectures/',
        include(lecture_patterns)
    ),
    path(
        'courses/<int:course_pk>/lectures/<int:lecture_pk>/',
        include(homework_patterns)
    ),
    path(
        'problems/',
        include(problem_patterns)
    )
]
 