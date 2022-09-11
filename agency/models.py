from django.db import models
from utils.models import CreateUpdateTracker


class Agency(CreateUpdateTracker):
	full_name = models.CharField(max_length=128, verbose_name="To'liq ismi: (F.I.SH)")
	address = models.CharField(max_length=256, verbose_name="Manzili: (shahar/tuman, ko'cha, uy)")
	phone = models.CharField(max_length=17, verbose_name="Telefon raqami: (+998 XX XXX XX XX)")
	image = models.ImageField(upload_to="media/", verbose_name="Fotosurat")
	image_passport = models.ImageField(upload_to="media/", verbose_name="Passportingiz fotosurati")

	def __str__(self) -> str:
		return self.full_name

	class Meta:
		verbose_name = "Agent"
		verbose_name_plural = "Agentlar"


class Market(CreateUpdateTracker):
	image_market = models.ImageField(upload_to="media/", verbose_name="Do'kon fotosurati")
	company_name = models.CharField(max_length=128, verbose_name="Firma nomi")
	company_document = models.ImageField(upload_to="media/", verbose_name="Firma hujjati: (Guvohnoma, Patent)") 
	full_name = models.CharField(max_length=128, verbose_name="To'liq ismi: (F.I.SH)")
	phone = models.CharField(max_length=17, verbose_name="Telefon raqami: (+998 XX XXX XX XX)")
	address = models.CharField(max_length=256, verbose_name="Manzili: (shahar/tuman, ko'cha, uy)")

	def __str__(self) -> str:
		return self.company_name

	class Meta:
		verbose_name = "Do'kon"
		verbose_name_plural = "Do'konlar"


class Product(CreateUpdateTracker):
	title = models.CharField(max_length=128, verbose_name="Nomi")
	price = models.CharField(max_length=128, verbose_name="narxi")
	amonut = models.CharField(max_length=128, verbose_name="miqdori")

	def __str__(self) -> str:
		return self.title

	class Meta:
		verbose_name = "mahsulot"
		verbose_name_plural = "mahsulotlar"


class ProductGiven(CreateUpdateTracker):
	market = models.ForeignKey(Market, on_delete=models.CASCADE, 
				related_name="product_given", verbose_name="Do'kon")
	product = models.ManyToManyField(Product, related_name="product")

	class Meta:
		verbose_name = "Berilgan mahsulot"
		verbose_name_plural = "Berilgan mahsulotlar"


class MoneyReceivedDebt(CreateUpdateTracker):
	market = models.ForeignKey(Market, on_delete=models.CASCADE, 
				related_name="money_received_debt", verbose_name="Do'kon")
	cash = models.PositiveIntegerField(max_length=128, verbose_name="Naqd")
	terminal = models.PositiveIntegerField(max_length=128, verbose_name="Terminal")
	contract = models.PositiveIntegerField(max_length=128, verbose_name="Shartnoma")
	get_all_money = models.CharField(max_length=128, verbose_name="Jami olingan pul")
	debt = models.CharField(max_length=128, verbose_name="Do'konning qarzi")

	class Meta:
		verbose_name = "Olingan pul va qarzdorlik"
		verbose_name_plural = "Olingan pullar va qarzdorliklar"


class PhotoReport(CreateUpdateTracker):
	market = models.ForeignKey(Market, on_delete=models.CASCADE, 
				related_name="photo_report", verbose_name="Do'kon")
	photo1 = models.ImageField(upload_to="media", verbose_name="Foto hisobot")
	photo2 = models.ImageField(upload_to="media", verbose_name="Foto hisobot", null=True, blank=True)

	class Meta:
		verbose_name = "Foto hisobot"
		verbose_name_plural = "Foto hisobotlar"