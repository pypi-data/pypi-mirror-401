Value Required INTERFACE (\S+)
Value ADMIN_STATUS (\S+)
Value OPER_STATUS (\S+)
Value Required POWER_DRAW ([0-9]*\.[0-9])
Value DEVICE_TYPE (\S+\s?\S+\s?\S+)
Value CLASS (\S+)
Value POWER_LIMIT ([0-9]*\.[0-9])

Start
 ^Interface\s+Admin\s+Oper\s+Power\s+Device\s+Class\s+Max -> Interface

Interface
 ^${INTERFACE}\s+${ADMIN_STATUS}\s+${OPER_STATUS}\s+${POWER_DRAW}\s+${DEVICE_TYPE}\s+${CLASS}\s+${POWER_LIMIT} -> Record
