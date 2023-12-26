from django.db import models


class RFIDCard(models.Model):
    card_number = models.CharField(max_length=50) 

    def __str__(self):
        return self.card_number 
    
class UserInfo(models.Model):
    card_number = models.CharField(max_length=20)
    name = models.CharField(max_length=100)
    email = models.EmailField(blank=True,null=True) 
    department = models.CharField(max_length=15,blank=True,null=True) 
    contact = models.IntegerField(blank=True, null=True)


    def __str__(self):
        return self.name
    

class UserLog(models.Model):
    user = models.ForeignKey(UserInfo, on_delete=models.CASCADE)
    entry_time = models.DateTimeField()
    leave_time = models.DateTimeField(null=True, blank=True)
    date = models.DateField()
    stay_time = models.DurationField(null=True, blank=True)

    def __str__(self):
        return f'{self.user.name} - {self.date}'
    
    def calculate_stay_time(self):
        if self.entry_time and self.leave_time:
            self.stay_time = self.leave_time - self.entry_time
            self.save()

    def save(self, *args, **kwargs):
        if not self.stay_time and self.leave_time:
            self.calculate_stay_time()
        super(UserLog, self).save(*args, **kwargs)