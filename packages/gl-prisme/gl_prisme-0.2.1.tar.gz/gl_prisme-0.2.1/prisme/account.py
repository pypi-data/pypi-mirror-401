from datetime import date
from typing import Dict, Iterator, List, TypeVar

from prisme.request import Request, Response
from prisme.util import parse_isodate


class AccountRequest(Request):
    def __init__(
        self,
        customer_id_number: int | str,
        from_date: date,
        to_date: date,
        open_closed: int = 2,
    ):
        super().__init__()
        self.customer_id_number = str(customer_id_number)
        self.from_date = from_date
        self.to_date = to_date
        self.open_closed = open_closed

    wrap = "CustTable"

    open_closed_map = {0: "Åbne", 1: "Lukkede", 2: "Åbne og Lukkede"}

    @property
    def dict(self) -> Dict[str, int | str | date]:
        return {
            "CustIdentificationNumber": self.customer_id_number,
            "FromDate": self.from_date,
            "ToDate": self.to_date,
            "CustInterestCalc": self.open_closed_map[self.open_closed],
        }


class AccountResponseTransaction(object):

    def __init__(self, data: Dict[str, str]):
        self.data = data
        self.account_number = data["AccountNum"]
        self.transaction_date = parse_isodate(data["TransDate"])
        self.accounting_date = parse_isodate(data["AccountingDate"])
        self.debitor_group_id = data["CustGroup"]
        self.debitor_group_name = data["CustGroupName"]
        self.voucher = data["Voucher"]
        self.text = data["Txt"]
        self.payment_code = data["CustPaymCode"]
        self.payment_code_name = data["CustPaymDescription"]
        amount = data["AmountCur"]
        try:
            self.amount = float(amount)
        except (ValueError, TypeError):
            self.amount = 0
        self.remaining_amount = data["RemainAmountCur"]
        self.due_date = data["DueDate"]
        self.closed_date = data["Closed"]
        self.last_settlement_voucher = data["LastSettleVoucher"]
        self.collection_letter_date = data["CollectionLetterDate"]
        self.collection_letter_code = data["CollectionLetterCode"]
        self.claim_type_code = data["ClaimTypeCode"]
        self.invoice_number = data["Invoice"]
        self.transaction_type = data["TransType"]
        self.extern_invoice_number = data.get("ExternalInvoiceNumber")


Transaction = TypeVar("Transaction", bound=AccountResponseTransaction)


class AccountResponse[Transaction](Response):

    def parse_transaction(self, data: Dict[str, str]) -> Transaction:
        raise NotImplementedError("Must be implemented in subclass")

    def __init__(self, request: AccountRequest, xml: str):
        super().__init__(request, xml)
        self.transactions: List[Transaction] = []
        if xml is not None:
            transactions = self.data["CustTable"]["CustTrans"]
            if type(transactions) is not list:
                transactions = [transactions]
            self.transactions = [self.parse_transaction(x) for x in transactions]

    def __iter__(self) -> Iterator[Transaction]:
        yield from self.transactions

    def __len__(self) -> int:
        return len(self.transactions)

    def __getitem__(self, index: int) -> Transaction:
        return self.transactions[index]


class SELAccountRequest(AccountRequest):

    method = "getAccountStatementSEL"

    @classmethod
    def response_class(cls) -> type[Response]:
        return SELAccountResponse


class SELAccountResponseTransaction(AccountResponseTransaction):

    def __init__(self, data: Dict[str, str]):
        super().__init__(data)
        self.rate_number = data.get("RateNmb")
        self.child_claimant = data.get("ChildClaimantFuj") or data.get("ChildClaimant")


class SELAccountResponse[Transaction](AccountResponse):

    def parse_transaction(self, data: Dict[str, str]) -> SELAccountResponseTransaction:
        return SELAccountResponseTransaction(data)

    def __init__(self, request: SELAccountRequest, xml: str):
        super().__init__(request, xml)

    def __getitem__(self, index: int) -> SELAccountResponseTransaction:
        return self.transactions[index]  # type: ignore[no-any-return]


class AKIAccountRequest(AccountRequest):

    method = "getAccountStatementAKI"

    @classmethod
    def response_class(cls) -> type[Response]:
        return AKIAccountResponse


class AKIAccountResponseTransaction(AccountResponseTransaction):

    def __init__(self, data: Dict[str, str]):
        super().__init__(data)
        self.claimant_name = data["ClaimantName"]
        self.claimant_id = data["ClaimantId"]
        self.child_claimant = data.get("ChildClaimant") or data.get("ChildClaimantFuj")


class AKIAccountResponse[Transaction](AccountResponse):

    def parse_transaction(self, data: Dict[str, str]) -> SELAccountResponseTransaction:
        return SELAccountResponseTransaction(data)

    def __init__(self, request: AKIAccountRequest, xml: str):
        super().__init__(request, xml)

    def __getitem__(self, index: int) -> AKIAccountResponseTransaction:
        return self.transactions[index]  # type: ignore[no-any-return]
