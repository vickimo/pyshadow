from pyshadow import *
import datetime

def testSunPosition():
    print("Testing: Sun Position")
    datet = datetime.datetime(2020, 4, 13, 16, 37, 0, tzinfo=datetime.timezone.utc)
    sun = SunPosition(datet, 2.36059, 48.85483)
    assert round(sun.altitude, 2) == 19.22
    assert round(sun.azimuth, 2) == 262.21

def testBuildingShadow():
    print("Testing: Shadow Calculation")
    datet = datetime.datetime(2020, 4, 13, 16, 37, 0, tzinfo=datetime.timezone.utc)
    building_polygon = [[2.321230990799024, 48.883737843553725], [2.32126610290205, 48.883662546380585], [2.321135396461886, 48.88363512484447], [2.3211004388451553, 48.883709751057076]]
    building_height = 10 # 10 meters
    sun = SunPosition(datet, building_polygon[0][0], building_polygon[0][1])
    building = EarthObject(building_height, building_polygon, sun)
    shadows = building.shadowPolygons
    assert (shadows[0] == [[2.321230990799024, 48.883737843553725], [2.32126610290205, 48.883662546380585], [2.321653813173527, 48.88369762336172], [2.321618701654243, 48.88377292053486]])

def main():
    print("Starting tests...")
    testSunPosition()
    testBuildingShadow()
    print("All tests passed!")

if __name__=="__main__":
    main()