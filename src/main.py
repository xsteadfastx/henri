import henri.__main__
from henri.network import create_ap, create_dns

create_ap()
create_dns()
henri.__main__.main(host="0.0.0.0", port="80")
