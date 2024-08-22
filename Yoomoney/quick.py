#     __  __           _         _              ____       _             _      _   
#    |  \/  | __ _  __| | ___   | |__  _   _   |  _ \ __ _| |_ _ __ ___ | | ___| |_ 
#    | |\/| |/ _` |/ _` |/ _ \  | '_ \| | | |  | |_) / _` | __| '__/ _ \| |/ _ \ __|
#    | |  | | (_| | (_| |  __/  | |_) | |_| |  |  __/ (_| | |_| | | (_) | |  __/ |_ 
#    |_|  |_|\__,_|\__,_|\___|  |_.__/ \__, |  |_|   \__,_|\__|_|  \___/|_|\___|\__|
#                                      |___/                                       

from yoomoney import Quickpay
from utils import read_file

data = read_file("config/settings.json")

def balance(sum: int, label: str) -> str:
    quickpay = Quickpay(
                receiver=data["yoomoney-id"],
                quickpay_form="shop",
                targets="Sponsor",
                paymentType="SB",
                sum=sum,
                successURL=data["bot-link"],
                label=label)
    return quickpay.base_url

