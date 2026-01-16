from datetime import date, datetime
from typing import Dict, List

from prisme.file import File
from prisme.request import Request, Response


class InvoiceLine:
    def __init__(
        self,
        description: str,
        beneficiary: str | None,
        quantity: int,
        unit_price: int,
        text: str,
        project: str | None,
        project_category: int | None,
        ledger_dimension: Dict[str, str | int],
    ):
        self.description = description
        self.beneficiary = beneficiary
        self.quantity = quantity
        self.unit_price = unit_price
        self.text = text
        self.project = project
        self.project_category = project_category
        self.ledger_dimension = ledger_dimension

    @property
    def dict(self) -> Dict[str, str | int | Dict[str, List[dict]] | None]:
        return {
            "Description": self.description,
            "Beneficiary": self.beneficiary,
            "Quantity": self.quantity,
            "UnitPrice": self.unit_price,
            "AmountCur": self.quantity * self.unit_price,
            "InvoiceTxt": self.text,
            "Project": self.project,
            "ProjCategoryId": self.project_category,
            "ledgerDimensionSegments": {
                "ledgerDimensionSegment": [
                    {"Name": key, "Value": value}
                    for key, value in self.ledger_dimension.items()
                ]
            },
        }


class InvoiceRequest(Request):
    def __init__(
        self,
        order_account_number: str,
        invoice_account_number: str,
        invoice_date: datetime | date,
        due_date: datetime | date,
        accounting_date: datetime | date,
        ledger_year: int,
        department_recid: int,
        invoice_ean: int,
        order_form_num: str,
        contact_person_id: str,
        currency_code: str,
        text: str,
        files: List[File],
        lines: List[InvoiceLine],
    ):
        self.order_account_number = order_account_number
        self.invoice_account_number = invoice_account_number
        self.invoice_date = (
            invoice_date
            if isinstance(invoice_date, datetime)
            else datetime.combine(invoice_date, datetime.min.time())
        )
        self.due_date = (
            due_date
            if isinstance(due_date, datetime)
            else datetime.combine(due_date, datetime.min.time())
        )
        self.accounting_date = (
            accounting_date
            if isinstance(accounting_date, datetime)
            else datetime.combine(accounting_date, datetime.min.time())
        )
        self.ledger_year = ledger_year
        self.department_recid = department_recid
        self.invoice_ean = invoice_ean
        self.order_form_num = order_form_num
        self.contact_person_id = contact_person_id
        self.currency_code = currency_code
        self.text = text
        self.files = files
        self.lines = lines

    wrap = "custinvoicetable"
    method = "createFreeTextInvoice"

    @property
    def dict(self) -> Dict[str, str | int | datetime | Dict[str, List[dict]]]:
        return {
            "OrderAccount": self.order_account_number,
            "InvoiceAccount": self.invoice_account_number,
            "InvoiceDate": self.invoice_date,
            "DueDate": self.due_date,
            "AccountingDate": self.accounting_date,
            "LedgerYear": self.ledger_year,
            "OMDepartmentRecIdExtFUJ": self.department_recid,
            "EinvoiceEANNum": self.invoice_ean,
            "PurchOrderFormNum": self.order_form_num,
            "ContactPersonId": self.contact_person_id,
            "CurrencyCode": self.currency_code,
            "InvoiceIntroTxt": self.text,
            "files": {"file": [file.dict for file in self.files]},
            "custinvoiceLines": {"custinvoiceLine": [line.dict for line in self.lines]},
        }


class InvoiceResponse(Response):

    def __init__(self, request: InvoiceRequest, xml: str):
        super().__init__(request, xml)
        if xml is not None:
            self.rec_id = int(self.data["CustInvoiceTable"]["RecId"])
