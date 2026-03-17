from django.contrib import admin
from .models import User
from channels_app.chanels import Channel, ChannelMember, ChannelInvite
admin.site.register(User)
admin.site.register(Channel)
admin.site.register(ChannelMember)
admin.site.register(ChannelInvite)