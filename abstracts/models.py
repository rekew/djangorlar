#Django modules
from django.db import models
from django.utils import timezone

    
class AbstractSoftDeletableModel(models.Model):
    """
    Abstract base model that implements soft delete behaviour.
    - Use .delete() to soft-delete (updates is_deleted and deleted_at)
    - Use .hard_delete() to actually delete
    - Use .restore() to restore
    """

    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null = True, blank = True)

    def delete(self):
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save(update_fields=["is_deleted", "deleted_at"])

    def hard_delete(self):
        super().delete()

    def restore(self):
        self.is_deleted = False
        self.deleted_at = None
        self.save(update_fields=["is_deleted", "deleted_at"])
    
    class Meta:
        abstract = True

class Course(AbstractSoftDeletableModel):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null = True)

class Student(AbstractSoftDeletableModel):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    course = models.ForeignKey(
        to='Course',           
        on_delete=models.CASCADE,
        related_name='students' 
    )