%% Rover 1 
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
rv.movingPower = 400; %W
rv.acceleration = 0.05; % m/s2
rv.powerCoef = 0.6; %W/kg

rv.baseMass = 105; %kg
rv.batterySize = 3000*3600; %watt-s
rv.chargingPower = -700; %W
rv.chargingDistance = 3; %m
rv.chargingDelay = 60; %sec
rv.depthOfDischarge = 0.5; % percent


%% Rover 2 
rv2=rover;

rv2.breakingRate = 70/3600; %kg/s
rv2.breakingPower = 150; %W
rv2.breakingSpeed = 0.01; %m/s
rv2.loadCapacity = 40; % kg

rv2.loadingRate = 220/3600; %kg/s
rv2.loadingPower = 200; %W

rv2.unloadingRate = 600/3600; %kg/s

rv2.speedCoef= -.00001; % (m/s)/kg
rv2.baseSpeed = 0.5 ; %m/s
rv2.movingPower = 400; %W
rv2.acceleration = 0.05; % m/s2
rv2.powerCoef = 0.6; %W/kg

rv2.baseMass = 105; %kg
rv2.batterySize = 3000*3600; %watt-s
rv2.chargingPower = -700; %W
rv2.chargingDistance = 3; %m
rv2.chargingDelay = 60; %sec
rv2.depthOfDischarge = 0.5; % percent


%% Rover buse elements
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
%% State bus elements

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

%% Simulation
out=sim("rvSim");
out2=sim("rv2Sim");








%% Plots

[int_modes, name_modes]=enumeration('modes');
subplot1=subplot(3,1,1);
% set time to x
x=out.simout.var.Power.Time./3600;
rv_color=[0 0.4470 0.7410];
rv2_color=[0.6350 0.0780 0.1840];

% Location 
y1_1 = out.simout.var.Location.Data;
y1_2 = out2.simout.var.Location.Data;
plot(x,y1_1)
hold on
plot(x,y1_2)


% Battery
subplot2=subplot(3,1,2); 
y2_1 = out.battery./rv.batterySize;
y2_2 = out2.battery./rv.batterySize;
plot(x,y2_1)
hold on 
plot(x, y2_2)
hold off

% Mode
subplot3=subplot(3,1,3); 
y3_1 = out.simout.gotoState.Data;
y3_2 = out2.simout.gotoState.Data;
plot(x,y3_1)
hold on
plot(x, y3_2)
hold off

ylabel(subplot1, 'Location (m)');
ylabel(subplot2, 'Battery %');
ylabel(subplot3, 'ConOp Mode'); 
set(subplot3,'YTickLabel',name_modes);
xlabel(subplot3, 'Time (hr)');
% 
% 
% averagePower=sum((out.simout.var.Power.Data>=0).*out.simout.var.Power.Data)/...
%     sum(out.simout.var.Power.Data>=0);
% 
% dailyPower=sum((out.simout.var.Power.Data>=0).*(out.simout.var.Power.Data))/3600/1000;%kWh
% totalPower=dailyPower*15*2; %kWh
% 
% idleTime=sum(out.simout.gotoState.Data==int8(modes.idle))/3600;
% disp(strcat("kg Delivered: ",string(max(out.total))));
% disp(strcat("Hours Charging: ", string(sum(out.simout.gotoState.Data==5)/3600)));
% disp(strcat("Average Power : ", string(averagePower)));
% disp(strcat("Idle Hours: ",string(idleTime)));