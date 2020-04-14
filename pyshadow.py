from pysolar import solar
import math

EARTH_RADIUS = 6378137 # in meters

# The sun position given the relative time and place on earth
class SunPosition:
    def __init__(self, date, longitude, latitude):
        self.date = date            # the datetime in question
        self.longitude = longitude  # the longitude in degrees of the earth location
        self.latitude = latitude    # the latitude in degrees of the earth location
    
    @property
    def altitude(self):
        self._altitude = solar.get_altitude(self.latitude, self.longitude, self.date)
        return self._altitude

    @property
    def azimuth(self):
        self._azimuth = solar.get_azimuth(self.latitude, self.longitude, self.date)
        return self._azimuth

# The structure to get the shadow of
class EarthObject:
    def __init__(self, height, polygon, sunPosition):
        self.height = height # height in meters
        self.polygon = polygon # type list, [longitude, latitude] {the vertices of the structure}
        self.sunPosition = sunPosition # sun position relative to the structure

    # returns list of shadow quadrilaterals for the structure
    @property
    def shadowPolygons(self): 
        azi_rad = math.radians(self.sunPosition.azimuth) # sun azimuth in radians
        L = self.shadowLength
        X_dif = -L * math.sin(azi_rad) # X diff in meters
        Y_dif = -L * math.cos(azi_rad) # Y diff in meters
        shadowVertices = [self.calcShadowLongLat(vertex[0], X_dif, vertex[1], Y_dif) for vertex in self.polygon]
        shadowPolygons = []
        # For each edge of polygon, get shadow edge -> combine for 1 shadow polygon
        for i in range(len(self.polygon)):
            i2 = i+1 if (i != len(self.polygon)-1) else 0
            vertex1 = self.polygon[i]
            vertex2 = self.polygon[i2]
            v1_shadow = shadowVertices[i]
            v2_shadow = shadowVertices[i2]
            shadowPolygons.append([vertex1, vertex2, v2_shadow, v1_shadow])
        return shadowPolygons # length = len(self.polygon) (#edges = #vertices)

    # return length of shadow in meters
    @property
    def shadowLength(self):
        alt_rad = math.radians(self.sunPosition.altitude) # convert to radians
        return self.height/math.tan(alt_rad)
    
    # return the shadow coordinates for a single vertex
    def calcShadowLongLat(self, old_long, x_diff, old_lat, y_diff):
        old_lat_rad = math.radians(old_lat)
        new_long = old_long + (math.degrees(x_diff / EARTH_RADIUS) / math.cos(old_lat_rad))
        new_lat = old_lat + math.degrees(y_diff / EARTH_RADIUS)
        return [new_long, new_lat]