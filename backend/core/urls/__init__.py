from core.urls import accounts, authentications, profiles


URL_COMPONENTS = (
    accounts.ACCOUNTS_URLS + authentications.AUTH_URLS + profiles.PROFILES_URLS
)


urlpatterns = URL_COMPONENTS

app_name = "core"
