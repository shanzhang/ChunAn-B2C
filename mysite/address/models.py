from django.db import models

# Create your models here.

class Address(models.Model):
    user_id = models.IntegerField()
    receiver_name = models.CharField(max_length=30)
    company_name = models.CharField(max_length=50)
    address_line_1 = models.TextField()
    address_line_2 = models.TextField()
    zip_code = models.CharField(max_length=10)
    city = models.CharField(max_length=50)
    province = models.CharField(max_length=20)
    phone = models.CharField(max_length=12)
    # email = models.EmailField()

    def __unicode__(self):
        return u"%s %s" % (self.id, self.user_id)


class AddressBook:
    def getAddressBook(self, search_user_id):
        return Address.objects.filter(user_id=search_user_id).order_by("id")

    def getAddress(self, search_id, search_userID):
        return Address.objects.get(id=search_id, user_id=search_userID)

    def insertAddress(self, userId, receiverName, addressLine_1, zipCode, City,
                      Province, Phone):
        address = Address(
            user_id = userId,
            receiver_name = receiverName,
            company_name = 'null',
            address_line_1 = addressLine_1,
            address_line_2 = 'null',
            zip_code = zipCode,
            city = City,
            province = Province,
            phone = Phone,
            # email=Email
        )
        address.save()

    def updateAddress(self, search_id, search_userID, receiverName, addressLine_1, zipCode, City, Province, Phone):
        address = self.getAddress(search_id, search_userID)
        address.receiver_name = receiverName
        address.company_name = 'null'
        address.address_line_1 = addressLine_1
        address.address_line_2 = 'null'
        address.zip_code = zipCode
        address.city = City
        address.province = Province
        address.phone = Phone
        # address.email = Email
        address.save()

    def deleteAddress(self, search_id, search_userID):
        address = self.getAddress(search_id, search_userID)
        address.delete()




