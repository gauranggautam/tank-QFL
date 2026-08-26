from montana import *
cryo = CryoCore("192.168.0.2")
pr = cryo.get_sample_chamber_pressure()
tp = cryo.get_user1_temperature()
tps = cryo.get_user1_temperature_stability()

print(pr)
print(tp)
print(tps)
