from xml.etree.ElementInclude import include
from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator
import bcrypt

class Users(models.Model):
    """
    The User model
    """
    id = fields.IntField(pk=True)
    first_name = fields.CharField(max_length=20, null=False)
    last_name = fields.CharField(max_length=50, null=False)
    join_date = fields.DateField(max_length = 50, null=False)
    password = fields.CharField(max_length=128, null=False)


# Response model 
User_Pydantic = pydantic_model_creator(Users, name="User", exclude=['password'])
# Request model
UserIn_Pydantic = pydantic_model_creator(Users, name="UserIn", exclude_readonly=True)