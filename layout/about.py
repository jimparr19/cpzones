import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc

about_layout = [
    dbc.Row(
        children=[
            dbc.Col(
                children=[
                    html.H1('About'),
                    dcc.Markdown('''
                    
                           I recently purchased a new smart watch to get motivated to start running again. I wanted a
                           watch that provided an estimate of running power, so I picked up a [COROS Pace 2](https://www.coros.com/pace2.php).
                           This watch seemed to have good reviews and I was on a bit of a budget with a 6 week old baby at home.
                           
                           I run lots of trails and training with heart rate always seems a bit delayed when hitting a hill 
                           and pacing strategies can be hard to stick to. Using power 
                           offers instantaneous feedback on my effort and it felt like a more intuitive way to set 
                           training zones and race strategies. 
                           
                           The problem I found is that it is difficult to know where to start with setting training 
                           zones based on power. Using [Stryd](https://www.stryd.com/en/) and their platform would help 
                           a lot with this but I didnt want to fork out for another device when I already had power
                           available to me on my watch. 
                           
                           A typical way to set power training zones in based on your Critical Power (CP). There are 
                           several ways to estimate your CP in order to determine your training zones but many of these 
                           seem over simplistic in order to calculate an accurate CP. Furthermore, they do not provide 
                           a level of confidence in the value generated so I wasn't sure if the data I collected was 
                           adequate and whether or not I would benefit from collecting some more.
                           
                           This website is aimed to help runners determine their CP and corresponding training zones. It 
                           attempts to use a scientific approach to compute an accurate CP but also highlights the 
                           uncertainty in this value so it can be used appropriately for setting training zones and race 
                           strategies.
                           
                           Using running power seems to be getting popular in running and more and more devices are 
                           offering a 'wrist-based' power estimate. I imagine it is only a matter of time before using 
                           power for running follows the world of cycling and becomes mainstream and hopefully this tool 
                           will be useful to individuals that find themselves in a similar position to me.
                           
                           '''
                                 )
                ]
            )
        ]
    ),
    html.Hr(),
    dbc.Row(
        children=[
            dbc.Col(
                children=[
                    html.H1('How to use this tool'),
                    dcc.Markdown('''
                    
                    Like many physical attributes, the confidence in my CP values should be an
                    
                    '''
                                 )
                ]
            )
        ]
    ),
    html.Hr(),
    dbc.Row(
        children=[
            dbc.Col(
                children=[
                    html.H1('The technical bit'),
                    dcc.Markdown('''
                    
                    Determining CP is a statistical problem where the confidence in the value calculated should improve as 
                    more evidence or information becomes available. This problem lends itself to a 
                    [Bayesian](https://en.wikipedia.org/wiki/Bayesian_inference) approach to determine 
                    CP and its uncertainty. 
                    
                    This tool gives the user an estimate of their CP but also indicates the level of uncertainty in this 
                    value. If there is large uncertainty, the user may want to improve this estimate by taking more 
                    measurements or reducing the variation between measurements by running more consistently or reducing 
                    the impact of fatigue on each interval.
                    
                    Let's start by looking at what information is available to determine CP before collecting any data. 
                    
                    One way to determine your CP is by using recent race results. Stryd provide this functionality on 
                    their platform but here we use [Riegel's Formula](https://en.wikipedia.org/wiki/Peter_Riegel) to 
                    determine an estimate for FTP (CP60 or CP at 60 minutes) based on a previous race result. 
                    
                    $$ \\frac{T_2}{T_1} = \\frac{D_2}{D_1}^\\alpha $$
                    
                    '''
                                 ),
                    html.P('''
                    
                    where the \(\\alpha\) is the fatigue factor which can vary between 1.05 and 1.08 depending on your 
                    level of fatigue resistance.
                    
                    '''
                           ),
                    dcc.Markdown('''
                    
                    From this formula, we can use a recent race result to determine the distance travelled when running 
                    for 60 minutes. We can then determine the 60 minute velocity and infer the power required to 
                    maintain this pace. Assuming flat terrain, this power is the CP60 determined from the formula 
                    
                    $$ CP60 = cvm + \\frac{1}{2} \\rho c_dAv^2 $$
                    
                    '''
                                 ),
                    html.P('''                    
                    where \(c\) is the specific energy cost of running in \(kJ/kg/km\), \(v\) is the 60 minute velocity 
                    in \(m/s\) determined from Riegel's Formula, \(m\) is the runner race weight in \(kg\), \(c_dA\) is 
                    the coefficient of drag times area in \(m^2\) and \(rho\) is the air density assumed to be 1.225 \(kg/m^3\).
                    '''
                           ),
                    dcc.Markdown('''
                    We incorporate some uncertainty in the specific energy cost of running (ranging between 0.88 and 
                    1.08), the coefficient of drag times area (ranging between 0.2 and 0.24) and the fatigue factor 
                    (ranging between 1.05 and 1.08) to determine an expected range for CP60.
                    
                    For a 70kg runner with a recent 5km race time of 20 minutes, the above formulas can be used to estimate 
                    a CP60 to be between 244 and 308 watts.
                    
                    **Note that FTP, CP60 and CP are often used interchangeably. In reality, FTP is equal to CP60 but CP 
                    should be lower as this is the maximum sustainable power at durations greater than 60 minutes. 
                    However, the difference between FTP and CP is often negligible given measurement error.**
                    
                    With no other information available, these formulas can be used to provide an approximate CP. 
                    Since we have some values that are uncertain and difficult to measure, the range in the CP is quite 
                    large, making it difficult to determine accurate power zones. 
                    
                    This estimate can however be improved by including some additional information using actual power 
                    measurements.
                    
                    Let's start by looking at some raw power data collected during a critical power test. Here I have 
                    run 3 intervals, each targeting a different power. I have tried to hold this power as consistent as 
                    possible and run at this power for as long as I could endure.
                    
                    ![](../assets/about/raw_example.png)
                    
                    This is slightly different to the **6/3 lap test** or **9/3minute test** outlined by 
                    [Stryd](https://support.stryd.com/hc/en-us/articles/115003989074-How-do-I-perform-a-Critical-Power-test-and-get-my-Critical-Power-and-Power-Zones-), 
                    as I find it easier to get consistent data choosing a target power and holding this for as long as possible. 
                    It doesnt matter what target power you choose but you should aim to collect data over a range of durations 
                    (ranging from a couple of minutes to over 10 minutes). You may wish to capture these intervals over 
                    multiple sessions which may help reduce the effect of fatigue on the CP estimates. 
                    
                    Next we select the data for each interval. Looking at a single interval, it is clear that there is 
                    some variation in the power during this period. It is actually quite difficult to consistently hold 
                    a target power but you should try and limit any large variations or drift in the power during the interval.
                    
                    Ideally, the power data should have a 
                    [normal distribution](https://en.wikipedia.org/wiki/Normal_distribution). This can be roughly judged 
                    using the histograms provided, where the power data should form a bell shaped distribution. 
                    
                    Plotting the energy consumed during each interval, we have a linear relationship. 
                    
                    Since we alredy have an estimate for CP from the recent race time, we use this to help inform a 
                    prior for our linear regression model.
                    
                    $$ P(\\theta|d) \\propto P(d|\\theta)P(\\theta) $$
                    
                    $$ y = \\theta_0 + \\theta_1x $$

                    $$ P(\\theta_0) = U(W'_l, W'_u) $$
                    $$ P(\\theta_1) = U(CP60_l, CP60_u) $$              
               
                    \* *Dijk, Hans; Megen, Ron; Rumery, Anne. The Secret of Running: maximum performance through effective power metering and training analysis, Meyer & Meyer Sport, 2017.*
                    '''
                    )
                ]
            )
        ]
    ),
    html.Hr(),
    dbc.Row(
        children=[
            dbc.Col(
                children=[
                    html.H1('What I run with'),
                    html.P('Some more notes here')
                ]
            )
        ]
    ),

]
