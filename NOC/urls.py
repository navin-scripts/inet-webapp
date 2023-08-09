from django.urls import path, include, re_path
from .views import unifi, unifilookup

app_name = 'NOC'

urlpatterns = [
    path('unifi/', unifi, name="unifi"),
    path('unifilookup/', unifilookup, name="unifilookup"),
]



'''

<div class="mb-5">
                        <div class="mb-4">
                            <span class="h5">Dark table</span>
                        </div>
                        <table class="table table-dark">
                            <tr>
                                <th scope="col" id="class1">Year</th>
                                <th scope="col" id="teacher1">Teacher</th>
                                <th scope="col" id="males1">Males</th>
                                <th scope="col" id="females1">Females</th>
                            </tr>
                            <tr>
                                <th scope="row" id="firstyear1" rowspan="2">First Year</th>
                                <th scope="row" id="Bolter1" headers="firstyear1 teacher1">D. Bolter</th>
                                <td headers="firstyear1 Bolter1 males1">5</td>
                                <td headers="firstyear1 Bolter1 females1">4</td>
                            </tr>
                            <tr>
                                <th scope="row" id="Cheetham1" headers="firstyear1 teacher1">A. Cheetham</th>
                                <td headers="firstyear1 Cheetham1 males1">7</td>
                                <td headers="firstyear1 Cheetham1 females1">9</td>
                            </tr>
                            <tr>
                                <th scope="row" id="secondyear1" rowspan="3">Second Year</th>
                                <th scope="row" id="Lam1" headers="secondyear1 teacher1">M. Lam</th>
                                <td headers="secondyear1 Lam1 males1">3</td>
                                <td headers="secondyear1 Lam1 females1">9</td>
                            </tr>
                            <tr>
                                <th scope="row" id="Crossy1" headers="secondyear1 teacher1">S. Crossy</th>
                                <td headers="secondyear1 Crossy1 males1">4</td>
                                <td headers="secondyear1 Crossy1 females1">3</td>
                            </tr>
                            <tr>
                                <th scope="row" id="Forsyth1" headers="secondyear1 teacher1">A. Forsyth</th>
                                <td headers="secondyear1 Forsyth1 males1">6</td>
                                <td headers="secondyear1 Forsyth1 females1">9</td>
                            </tr>
                        </table>
                    </div>

'''