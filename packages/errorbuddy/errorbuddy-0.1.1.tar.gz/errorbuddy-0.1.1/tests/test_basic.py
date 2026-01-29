from errorbuddy import explain

try:
    x = 10 + "5"
except Exception as e:
    explain(e)