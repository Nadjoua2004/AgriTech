from django.db import models

class Worker(models.Model):
    WORKER_TYPE_CHOICES = [
        ('field_worker',        'Field Worker'),
        ('irrigation_worker',   'Irrigation Worker'),
        ('equipment_operator',  'Equipment Operator'),
        ('supervisor',          'Supervisor'),
        ('farm_manager',        'Farm Manager'),
        ('agronomist',          'Agronomist'),
        ('quality_inspector',   'Quality Inspector'),
    ]
    STATUS_CHOICES = [
        ('active',   'Active'),
        ('inactive', 'Inactive'),
        ('on_leave', 'On Leave'),
    ]

    first_name   = models.CharField(max_length=100)
    last_name    = models.CharField(max_length=100)
    phone        = models.CharField(max_length=20)
    hire_date    = models.DateField()
    worker_type  = models.CharField(max_length=50, choices=WORKER_TYPE_CHOICES)
    status       = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    zone         = models.CharField(max_length=100, blank=True)   # which area of the farm
    user_id      = models.IntegerField(null=True, blank=True)     # links to Nadjoua's auth user
    created_at   = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.worker_type})"

class DailyTask(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('done', 'Done'),
        ('missed', 'Missed'),
    ]

    worker       = models.ForeignKey(Worker, on_delete=models.CASCADE, related_name='tasks')
    date         = models.DateField()
    description  = models.TextField()
    status       = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    assigned_by  = models.IntegerField()     # supervisor's user_id from JWT — no FK
    
    # External service references — plain integers, NO ForeignKey
    land_id      = models.IntegerField(null=True, blank=True)       # Sarah's service
    culture_id   = models.IntegerField(null=True, blank=True)       # Nadjoua's service
    equipment_id = models.IntegerField(null=True, blank=True)       # Sid Ahmed's service

    created_at   = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Task {self.id} for {self.worker.first_name} on {self.date}"

class WorkHours(models.Model):
    worker        = models.ForeignKey(Worker, on_delete=models.CASCADE, related_name='hours')
    date          = models.DateField()
    hours_worked  = models.DecimalField(max_digits=5, decimal_places=2)
    overtime      = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    notes         = models.TextField(blank=True)

    class Meta:
        unique_together = ['worker', 'date']   # one entry per worker per day

    def __str__(self):
        return f"{self.hours_worked}h for {self.worker.first_name} on {self.date}"

class Salary(models.Model):
    worker       = models.ForeignKey(Worker, on_delete=models.CASCADE, related_name='salaries')
    month        = models.DateField()          # store as first day of the month e.g. 2024-04-01
    base_salary  = models.DecimalField(max_digits=10, decimal_places=2)
    bonus        = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    overtime_pay = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    deductions   = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total        = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def save(self, *args, **kwargs):
        # Auto calculate total before saving
        self.total = self.base_salary + self.bonus + self.overtime_pay - self.deductions
        super().save(*args, **kwargs)

    class Meta:
        unique_together = ['worker', 'month']

    def __str__(self):
        return f"Salary {self.month.strftime('%Y-%m')} for {self.worker.first_name} - {self.total}"
