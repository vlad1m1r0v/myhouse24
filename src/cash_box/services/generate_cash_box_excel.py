from datetime import datetime

import openpyxl
from openpyxl.styles import Font, Alignment, Border, Side
from io import BytesIO


def generate_cash_box_excel(transactions):
    wb = openpyxl.Workbook()
    ws = wb.active

    ws.column_dimensions["A"].width = 20
    ws.column_dimensions["B"].width = 20
    ws.column_dimensions["C"].width = 15
    ws.column_dimensions["D"].width = 25
    ws.column_dimensions["E"].width = 25
    ws.column_dimensions["F"].width = 20
    ws.column_dimensions["G"].width = 25
    ws.column_dimensions["H"].width = 15

    headers = ['№', 'Дата', 'Статус', 'Тип платежу', 'Власник', 'Особовий рахунок', 'Витрата / Витрата', 'Cума']

    ws.append(headers)

    for record in transactions:
        record_date = datetime.strptime(str(record.date), "%Y-%m-%d")
        formatted_date = record_date.strftime("%d.%m.%Y")

        ws.append(
            [
                record.no,
                formatted_date,
                'Проведена' if record.is_complete else 'Не проведена',
                record.payment_item.name,
                str(record.owner) if record.owner else 'Не вказано',
                record.personal_account.no if record.personal_account else 'Не вказано',
                record.get_type_display(),
                record.amount
            ])

        for cell in ws[1:1]:
            cell.alignment = Alignment(horizontal='center')
            cell.font = Font(bold=True)

    output = BytesIO()
    wb.save(output)
    output.seek(0)
    return output
