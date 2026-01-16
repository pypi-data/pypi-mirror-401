

from telonex import get_dataframe, get_availability

key = "tlx_0de481c6ddf7231b54f75941f61eaefe"

availability = get_availability(exchange="polymarket", asset_id="34263170192678509613984142997412052653559758038927875904042796579650705664225")

print(availability)

df = get_dataframe(
    api_key=key,
    exchange="polymarket",
    channel="onchain_fills",
    asset_id="34263170192678509613984142997412052653559758038927875904042796579650705664225",
    from_date="2025-11-28",
    to_date="2026-01-10",
    verbose=True
)



print(len(df))
print(df.head(10))
