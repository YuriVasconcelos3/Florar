from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField

STATUS = ((0, 'Draft'), (1, 'Published'))

class Post(models.Model):
    image = models.ImageField(upload_to="postagem/", unique=True)
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    created_on = models.DateField(auto_now_add=True)
    update_on = models.DateField(auto_now=True)
    content = RichTextField()
    status = models.IntegerField(choices=STATUS, default=0)
    display_id = models.PositiveIntegerField(unique=True, editable=False)

    class Meta:
        ordering = ['-created_on']

    def save(self, *args, **kwargs):
        if not self.pk:  # Only on creation
            last_post = Post.objects.order_by('-display_id').first()
            if last_post:
                self.display_id = last_post.display_id + 1
            else:
                self.display_id = 1
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        # Update display_id for subsequent posts
        subsequent_posts = Post.objects.filter(display_id__gt=self.display_id)
        subsequent_posts.update(display_id=models.F('display_id') - 1)

    def __str__(self):
        return self.title
