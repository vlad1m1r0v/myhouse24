from django.db.models import Q

from src.flats.models import Flat
from src.payment_receipts.models import Receipt
from src.user_messages.models import ReadMessage, Message


def account_information(request):
    if all([
        request.user.is_authenticated,
        not request.user.is_superuser,
        not request.user.is_staff]):
        user = request.user

        has_debt = (Receipt.objects
                    .filter(status__in=['unpaid', 'partially_paid'], flat__owner=user)
                    .select_related('flat', 'flat__owner')
                    .exists())

        flats = Flat.objects.filter(owner=user.id).select_related('house', 'section', 'floor', 'owner')

        houses_ids = [flat.house.id for flat in flats]
        sections_ids = [flat.section.id for flat in flats]
        floors_ids = [flat.floor.id for flat in flats]
        flats_ids = [flat.id for flat in flats]


        read_messages = ReadMessage.objects.filter(user=user.id).values_list('message_id', flat=True)

        filters = Q()

        filters |= Q(
            house__isnull=True,
            section__isnull=True,
            floor__isnull=True,
            flat__isnull=True,
            flat_owner__isnull=True
        )

        filters |= Q(
            house__in=[*houses_ids],
            section__isnull=True,
            floor__isnull=True,
            flat__isnull=True,
            flat_owner__isnull=True
        )

        filters |= Q(
            house__in=[*houses_ids],
            section__in=[*sections_ids],
            floor__isnull=True,
            flat__isnull=True,
            flat_owner__isnull=True
        )

        filters |= Q(
            house__in=[*houses_ids],
            section__in=[*sections_ids],
            floor__in=[*floors_ids],
            flat__isnull=True,
            flat_owner__isnull=True
        )

        filters |= Q(
            house__in=[*houses_ids],
            section__in=[*sections_ids],
            floor__in=[*floors_ids],
            flat__in=[*flats_ids],
            flat_owner__isnull=True
        )

        filters |= Q(
            house__isnull=True,
            section__isnull=True,
            floor__isnull=True,
            flat__isnull=True,
            flat_owner=user
        )

        # to_debtors=True is only for users who have debt.
        # to_debtors=False is for all users.
        if not has_debt:
            filters &= Q(to_debtors=False)

        filters &= ~Q(id__in=read_messages)

        messages = Message.objects.filter(filters)

        return {
            'unread_messages': messages,
            'flats': flats
        }

    return {}







