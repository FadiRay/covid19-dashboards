from covid19 import conn, SelectedDate, SelectedCountry, SelectedParameter

def test_connection():
    assert conn()[0]==200, 'no response from the covid19 data'
    assert conn()[1]==200, 'no response from geojson'
    assert SelectedDate()==True, 'Error by selecting the date'
    assert SelectedCountry()==True, 'Error by selecting the country'
    assert SelectedParameter()==True, 'Error by selecting Cases/Deaths'
    
    