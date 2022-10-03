


rv=rover;

rv.breakingRate = 70/3600; %kg/s
rv.breakingPower = 150; %W
rv.breakingSpeed = 0.01; %m/s
rv.loadCapacity = 40; % kg

rv.loadingRate = 220/3600; %kg/s
rv.loadingPower = 200; %W

rv.unloadingRate = 600/3600; %kg/s

rv.speedCoef= -.00001; % (m/s)/kg
rv.baseSpeed = 0.5 ; %m/s
rv.movingPower = 350; %W
rv.acceleration = 0.05; % m/s2
rv.powerCoef = 0.6; %W/kg

rv.baseMass = 105; %kg
rv.batterySize = 3000*3600; %watt-s
rv.chargingPower = -650; %W
rv.chargingDistance = 3; %m
rv.chargingDelay = 60; %sec
rv.depthOfDischarge = 0.5; % percent

rvelem(1)=Simulink.BusElement;
rvelem(1).Name = 'batterySize';
rvelem(1).DataType = "double";

rvelem(2)=Simulink.BusElement;
rvelem(2).Name = 'chargingDistance';
rvelem(2).DataType = "double";

rvelem(3)=Simulink.BusElement;
rvelem(3).Name = 'loadCapacity';
rvelem(3).DataType = "double";

rvelem(4)=Simulink.BusElement;
rvelem(4).Name = 'chargingDelay';
rvelem(4).DataType = "double";

rvelem(5)=Simulink.BusElement;
rvelem(5).Name = 'depthOfDischarge';
rvelem(5).DataType = "double";



bus_rv = Simulink.Bus;
bus_rv.Elements = rvelem;




elem(1)=Simulink.BusElement;
elem(1).Name = 'Power';
elem(1).DataType = "double";

elem(2)=Simulink.BusElement;
elem(2).Name = 'Location';
elem(2).DataType = "double";

elem(3)=Simulink.BusElement;
elem(3).Name = 'Loaded_Mass';
elem(3).DataType = "double";

elem(4)=Simulink.BusElement;
elem(4).Name = 'Excavated_Mass';
elem(4).DataType = "double";

elem(5)=Simulink.BusElement;
elem(5).Name = 'State';
elem(5).DataType = "int8";

elem(6)=Simulink.BusElement;
elem(6).Name = 'gotoState';
elem(6).DataType = "int8";

curState = Simulink.Bus;
curState.Elements = elem;


out=sim("roverSim");

subplot(3,1,1);
x=out.simout.var.Power.Time./3600;

y1 = out.simout.var.Location.Data;
plot(x,y1)

subplot(3,1,2); 
y2 = out.battery./rv.batterySize;
%y2= out.simout.var.Loaded_Mass.Data;
plot(x,y2)

subplot(3,1,3); 
y3 = out.simout.gotoState.Data;
plot(x,y3)


averagePower=sum((out.simout.var.Power.Data>=0).*out.simout.var.Power.Data)/...
    sum(out.simout.var.Power.Data>=0);

idleTime=sum(out.simout.gotoState.Data==int8(modes.idle))/3600;
disp(strcat("kg Delivered: ",string(max(out.total))));
disp(strcat("Hours Charging: ", string(sum(out.simout.gotoState.Data==5)/3600)));
disp(strcat("Average Power : ", string(averagePower)));
disp(strcat("Idle Hours: ",string(idleTime)));