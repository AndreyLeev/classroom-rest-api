from django.db import models
from django.conf import settings 


def user_directory_path(instance, filename):
    """Get path MEDIA_ROOT/materials/<username>/<filename>"""
    return f'materials/{instance.creator.username}/{filename}'


class Course(models.Model):    
    title = models.CharField(max_length=255)
    description = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
   
    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='courses'
    )

    class Meta:
        verbose_name_plural = 'courses'
        ordering = ['-date_created']

    def __str__(self):
        return f'{self.title}'


class Lecture(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    file = models.FileField(
        upload_to=user_directory_path,
        null=True
    )

    course = models.ForeignKey(
        'Course',
        on_delete=models.CASCADE
    )
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True
    )

    class Meta:
        verbose_name_plural = 'lectures'
        unique_together = [['course','title'],]
        ordering = ['-date_created']

    def __str__(self):
        return f'{self.title}'


class Problem(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    deadline = models.DateTimeField(null=True)
    
    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through='ProblemUserMembership',
    )   
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='problems',
    )
    lecture = models.ForeignKey(
        'Lecture',
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name_plural = 'problems'
        unique_together = [['lecture','title'],]
        ordering = ['date_created', '-deadline'] 

    def __str__(self):
        return f'{self.title}'


class ProblemUserMembership(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    problem = models.ForeignKey(
        'Problem',
        on_delete=models.CASCADE
    )
    
    done_status = models.BooleanField(default=False)
    accept_status = models.BooleanField(default=False)
    mark = models.SmallIntegerField(default=0)


class ProblemSolution(models.Model):
    solution = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)

    problem = models.OneToOneField(
        'ProblemUserMembership',
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = 'solution'
        verbose_name_plural = 'solutions'


class Comment(models.Model):
    text = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    ) 
    problem = models.ForeignKey(
        'ProblemUserMembership',
        on_delete=models.CASCADE,
        related_name='comments',
    )

    class Meta:
        verbose_name = 'comment'
        verbose_name_plural = 'comments'
        ordering = ['date_created',]  