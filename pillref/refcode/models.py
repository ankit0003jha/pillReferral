from django.db import models
import datetime
from django.contrib.auth.models import User
import uuid


class Profile(models.Model):

   
    user = models.OneToOneField(User,related_name='profile',on_delete=models.CASCADE)
    referral_code = models.CharField(max_length=8, blank=True)
    referred_by = models.ForeignKey(User, on_delete=models.CASCADE,blank=True, null=True, related_name= "ref_by")
    created_on = models.DateTimeField(auto_now_add=True)
    incentives = models.IntegerField(default=0, blank=True, null=True)

    def __str__(self):
        return  f"{self.user.username}-{self.referral_code}"


    def get_recommened_profiles(self):
	    qs = Profile.objects.all()
	    my_refered = []
	    for profile in qs:
		    if profile.referred_by == self.user:
			    my_refered.append(profile)
	    return my_refered


    def save(self, *args, **kwargs):
        if self.referral_code == "":
            referral_code = str(uuid.uuid4()).replace("-", "")[:8]
            self.referral_code = referral_code
        super().save(*args, **kwargs)
