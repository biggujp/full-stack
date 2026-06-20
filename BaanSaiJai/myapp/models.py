from django.db import models
from django.contrib.auth.models import User

class Incident(models.Model):
    CATEGORY_CHOICES = [
        ('electric', 'ไฟฟ้า'),
        ('water', 'ประปา'),
        ('road', 'ถนน'),
        ('security', 'ความปลอดภัย'),
        ('clean', 'ความสะอาด'),
        ('other', 'อื่น ๆ'),
    ]

    PRIORITY_CHOICES = [
        ('low', 'ต่ำ'),
        ('medium', 'ปานกลาง'),
        ('high', 'สูง'),
        ('urgent', 'เร่งด่วน'),
    ]

    STATUS_CHOICES = [
        ('new', 'แจ้งใหม่'),
        ('received', 'รับเรื่องแล้ว'),
        ('progress', 'กำลังดำเนินการ'),
        ('completed', 'แก้ไขเสร็จ'),
        ('closed', 'ปิดงาน'),
    ]

    code = models.CharField(
        max_length=30,
        unique=True,
        verbose_name='เลขที่แจ้งเหตุ'
    )

    title = models.CharField(
        max_length=255,
        verbose_name='หัวข้อ'
    )

    description = models.TextField(
        verbose_name='รายละเอียด'
    )

    location = models.CharField(
        max_length=255,
        verbose_name='สถานที่'
    )

    reporter_name = models.CharField(
        max_length=150,
        verbose_name='ผู้แจ้ง'
    )

    reporter_phone = models.CharField(
        max_length=20,
        blank=True,
        verbose_name='เบอร์โทร'
    )

    category = models.CharField(
        max_length=30,
        choices=CATEGORY_CHOICES,
        default='other',
        verbose_name='ประเภท'
    )

    priority = models.CharField(
        max_length=20,
        choices=PRIORITY_CHOICES,
        default='medium',
        verbose_name='ความเร่งด่วน'
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='new',
        verbose_name='สถานะ'
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='วันที่แจ้ง'
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='อัปเดตล่าสุด'
    )

    closed_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='วันที่ปิดงาน'
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'แจ้งเหตุ'
        verbose_name_plural = 'รายการแจ้งเหตุ'

    def __str__(self):
        return f'{self.code} - {self.title}'


class IncidentProgress(models.Model):
    incident = models.ForeignKey(
        Incident,
        on_delete=models.CASCADE,
        related_name='progresses',
        verbose_name='รายการแจ้งเหตุ'
    )

    status = models.CharField(
        max_length=20,
        choices=Incident.STATUS_CHOICES,
        verbose_name='สถานะ'
    )

    note = models.TextField(
        verbose_name='บันทึกการดำเนินงาน'
    )

    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='ผู้บันทึก'
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='วันที่บันทึก'
    )

    class Meta:
        ordering = ['created_at']
        verbose_name = 'ติดตามผล'
        verbose_name_plural = 'ประวัติการติดตามผล'

    def __str__(self):
        return f'{self.incident.code} - {self.get_status_display()}'



class IncidentProgress(models.Model):
    incident = models.ForeignKey(Incident, on_delete=models.CASCADE, related_name='progresses', verbose_name='รายการแจ้งเหตุ')
    status = models.CharField(max_length=20, choices=Incident.STATUS_CHOICES, verbose_name='สถานะ')
    note = models.TextField(verbose_name='บันทึกการดำเนินงาน')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='ผู้บันทึก')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='วันที่บันทึก')

    class Meta:
        ordering = ['created_at']
        verbose_name = 'ติดตามผล'
        verbose_name_plural = 'ประวัติการติดตามผล'

    def __str__(self):
        return f'{self.incident.code} - {self.get_status_display()}'

# Create your models here.
# class Member(models.Model):
#     name = models.CharField(max_length=100)
#     homenum = models.CharField(max_length=6)
#     email = models.EmailField()
#     phone = models.CharField(max_length=10)
#     point = models.IntegerField(default=1)
#     address = models.TextField(null=True, blank=True)

#     def __str__(self):        
#         return 'ชื่อ: {} | บ้านเลขที่: {} | โทร: {}'.format(self.name, self.homenum, self.phone)

