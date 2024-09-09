from .payment_items import (AdminPaymentItemsView,
                            AdminPaymentItemsDatatableView,
                            AdminPaymentItemsDatatableView,
                            AdminPaymentItemCreateView,
                            AdminPaymentItemUpdateView,
                            AdminPaymentItemsDeleteView)

from .payment_credential import AdminPaymentCredentialView

from .users import (AdminUsersView,
                    AdminUsersDatatableView,
                    AdminUserDetailView,
                    AdminUserCreateView,
                    AdminUserUpdateView,
                    AdminUserDeleteView)

from .permissions import AdminGroupPermissionsView

from .services import AdminServicesView

from .tariffs import (AdminTariffsView,
                      AdminTariffsDatatableView,
                      AdminTariffDetailView,
                      AdminTariffUpdateView,
                      AdminTariffCreateView,
                      AdminTariffDeleteView)