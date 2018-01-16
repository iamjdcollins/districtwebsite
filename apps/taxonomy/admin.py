from django.contrib import admin
from guardian.admin import GuardedModelAdmin
from mptt.admin import MPTTModelAdmin
from .models import Location, City, State, Zipcode, Language, TranslationType, SchoolType, OpenEnrollmentStatus, BoardPrecinct, BoardMeetingType, BoardPolicySection, DistrictCalendarEventCategory, DistrictLogoGroup, DistrictLogoStyleVariation, SchoolOption

class LocationAdmin(MPTTModelAdmin,GuardedModelAdmin):
  pass

class CityAdmin(MPTTModelAdmin,GuardedModelAdmin):
  pass

class StateAdmin(MPTTModelAdmin,GuardedModelAdmin):
  pass

class ZipcodeAdmin(MPTTModelAdmin,GuardedModelAdmin):
  pass

class LanguageAdmin(MPTTModelAdmin,GuardedModelAdmin):
  pass

class TranslationTypeAdmin(MPTTModelAdmin,GuardedModelAdmin):
  pass

class SchoolTypeAdmin(MPTTModelAdmin,GuardedModelAdmin):
  pass

class OpenEnrollmentStatusAdmin(MPTTModelAdmin,GuardedModelAdmin):
  pass

class BoardPrecinctAdmin(MPTTModelAdmin,GuardedModelAdmin):
  pass

class BoardMeetingTypeAdmin(MPTTModelAdmin,GuardedModelAdmin):
  pass

class BoardPolicySectionAdmin(MPTTModelAdmin,GuardedModelAdmin):
  pass

class DistrictCalendarEventCategoryAdmin(MPTTModelAdmin,GuardedModelAdmin):
  pass

class DistrictLogoGroupAdmin(MPTTModelAdmin,GuardedModelAdmin):
  pass

class DistrictLogoStyleVariationAdmin(MPTTModelAdmin,GuardedModelAdmin):
  pass

class SchoolOptionAdmin(MPTTModelAdmin, GuardedModelAdmin):
  pass

admin.site.register(Location, LocationAdmin)
admin.site.register(City, CityAdmin)
admin.site.register(State, StateAdmin)
admin.site.register(Zipcode, ZipcodeAdmin)
admin.site.register(Language, LanguageAdmin)
admin.site.register(TranslationType, TranslationTypeAdmin)
admin.site.register(SchoolType, SchoolTypeAdmin)
admin.site.register(OpenEnrollmentStatus, OpenEnrollmentStatusAdmin)
admin.site.register(BoardPrecinct, BoardPrecinctAdmin)
admin.site.register(BoardMeetingType, BoardMeetingTypeAdmin)
admin.site.register(BoardPolicySection, BoardPolicySectionAdmin)
admin.site.register(DistrictCalendarEventCategory, DistrictCalendarEventCategoryAdmin)
admin.site.register(DistrictLogoGroup, DistrictLogoGroupAdmin)
admin.site.register(DistrictLogoStyleVariation, DistrictLogoStyleVariationAdmin)
admin.site.register(SchoolOption, SchoolOptionAdmin)
