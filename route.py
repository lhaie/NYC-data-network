

class Route:
    def __init__(self, D):
        self.dropoff_datetime = D['tpep_dropoff_datetime']
        self.dropoff_latitude = float(D['dropoff_latitude'])
        self.dropoff_longitude = float(D['dropoff_longitude'])
        self.extra = float(D['extra'])
        self.fare_amount = float(D['fare_amount'])
        self.mta_tax = float(D['mta_tax'])
        self.passenger_count = int(D['passenger_count'])
        self.payment_type = D['payment_type']
        self.pickup_datetime = D['tpep_pickup_datetime']
        self.pickup_latitude = float(D['pickup_latitude'])
        self.pickup_longitude = float(D['pickup_longitude'])
        self.ratecodeid = D['RateCodeID']
        self.store_and_fwd_flag = D['store_and_fwd_flag']
        self.tip_amount = float(D['tip_amount'])
        self.tolls_amount = float(D['tolls_amount'])
        self.total_amount = float(D['total_amount'])
        self.trip_distance = float(D['trip_distance'])
        self.vendor_id = D['VendorID']
    
class Route_sample:
    def __init__(self, D):
        self.dropoff_datetime = D['dropoff_datetime']
        self.dropoff_latitude = float(D['dropoff_latitude'])
        self.dropoff_longitude = float(D['dropoff_longitude'])
        self.extra = float(D['extra'])
        self.fare_amount = float(D['fare_amount'])
        self.imp_surcharge = float(D['imp_surcharge'])
        self.mta_tax = float(D['mta_tax'])
        self.passenger_count = int(D['passenger_count'])
        self.payment_type = D['payment_type']
        self.pickup_datetime = D['pickup_datetime']
        self.pickup_latitude = float(D['pickup_latitude'])
        self.pickup_longitude = float(D['pickup_longitude'])
        self.ratecodeid = D['ratecodeid']
        self.store_and_fwd_flag = D['store_and_fwd_flag']
        self.tip_amount = float(D['tip_amount'])
        self.tolls_amount = float(D['tolls_amount'])
        self.total_amount = float(D['total_amount'])
        self.trip_distance = float(D['trip_distance'])
        self.vendor_id = D['vendor_id']

    
        