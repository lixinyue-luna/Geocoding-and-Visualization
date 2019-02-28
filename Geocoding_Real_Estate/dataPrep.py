import cPickle as pickle
import pandas as pd
import urllib, time, json, ssl

FILE = 'Data_Step1_8'
df = pickle.load(open(FILE,'rb')) # Pandas dataframe
# print list(df)    # Print out headers
print len(df)   # Number of records

# Get ungeocoded data everytime
# Use DataID as unique identifier
unlocated = df.loc[df.lat == 0,[u'DataId',u'State', u'County',u'City', u'Address',u'PostalCode','Location','lat','lng']]
unlocated = unlocated.sort_values('Location',na_position='first')
print '# of unlocated: ', len(unlocated), '\n'

# # Debug
# print unlocated.head()
# print unlocated.tail()

# Geocoding:
serviceurl = 'https://maps.googleapis.com/maps/api/geocode/json?'
# Deal with SSL certificate anomalies Python > 2.7
scontext = ssl.SSLContext(ssl.PROTOCOL_TLSv1)

limit = 2500 if len(unlocated) > 2500 else len(unlocated)
city_exceptions = ['Outside Area (Inside Ca)', 'Outside Area (Outside Ca)', None]
county_exceptions = ['Other County', 'Other State']
state_exceptions = ['OR']
# limit = 0  # For testing
count = 0
while count < limit:
    location = unlocated.iloc[count, unlocated.columns.get_loc('Location')]
    try:
        if location != 'zz_OVER_QUERY_LIMIT' and location != 'zz_OK' and location[0:3] == 'zz_':
            print 'Reached bottleneck'
            break
    except:
        pass
    idnr = unlocated.iloc[count, unlocated.columns.get_loc('DataId')]
    address = unlocated.iloc[count, unlocated.columns.get_loc('Address')]
    city = unlocated.iloc[count, unlocated.columns.get_loc('City')]
    state = unlocated.iloc[count, unlocated.columns.get_loc('State')]
    zipcode = int(unlocated.iloc[count, unlocated.columns.get_loc('PostalCode')])

    # construct query to api
    if city not in city_exceptions and state not in state_exceptions:
        city = city.replace(' Area', '')
        query = ', '.join((address, city, state))
    elif city not in city_exceptions and state in state_exceptions:
        city = city.replace(' Area', '')
        query = ', '.join((address, city))
    elif city in city_exceptions and state not in state_exceptions:
        query = ', '.join((address, state))
    else:
        query = address

    # Request to googleapis
    print 'Resolving', query
    url = serviceurl + urllib.urlencode({"sensor":"false", "address": query})
    uh = urllib.urlopen(url, context=scontext)
    entry = uh.read()
    count += 1
    print 'Retrieved',len(entry)
    try:
        js = json.loads(str(entry))
        # print js #  Uncomment this line to print js in case unicode causes an error
    except:
        continue

    # Read status
    if 'status' not in js:
        print '==== Failure To Retrieve (no status) ====\n'
        continue
    if js['status'] != 'OK':
        df.loc[df.DataId == idnr, 'Location'] = 'zz_' + js['status']
        print '==== Failure To Retrieve (' + js['status'] + ') ====\n'
        continue

    # js['results'] == 'OK', read data
    lat = js['results'][0]['geometry']['location']['lat']
    lng = js['results'][0]['geometry']['location']['lng']
    location = 'POINT(' + str(lat) + ' ' + str(lng) + ')'
    where = js['results'][0]['formatted_address']
    address_components = js['results'][0]['address_components']
    try:
        component_postal = filter(lambda x: x['types'] == ['postal_code'], address_components)
        postal = int(component_postal[0]['long_name'])
        print 'Postal code found in js.'
        if postal != zipcode:
            location = location + '_PostalCode_' + str(zipcode)
            print 'Postal codes do not match: ', postal, zipcode, where, '\n'
        else:
            print 'Postal code matched.'
    except:
        print 'Postal code not found in js.'
        pass
    # Write results to dataframe
    df.loc[df.DataId == idnr, 'lat'] = lat
    df.loc[df.DataId == idnr, 'lng'] = lng
    df.loc[df.DataId == idnr, 'Location'] = location
    print 'Retrieved #', count, ': ', where, '\n'

    if count%500 == 0:
        pickle.dump(df, open(FILE, 'wb'))
        print 'Pickled #', count
    time.sleep(0.03)

pickle.dump(df, open(FILE, 'wb'))
print 'Pickled'


# df2 = df.sort_values('lat').lat
# # df.plot.scatter(x='lat',y='lng')
# df2.plot.hist()
# plt.show()
