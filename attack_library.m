yalmip('clear')

n=2;
m=1;
p=1;

A=[1,0.1;0,1];
B=[0.005;0.1];
C=[1 0];
K=[16.0302,5.6622];
L=[1.8721;9.6532];
Th=0.003;
Y=60;
U=1200;
x_min=[-30;-25];
x_max=[30;25];
nums=1000;
dataset=zeros(2,16,nums);
t=5;
for sam=1:nums
    t=5;
    x0 = x_min + (x_max - x_min) .* rand(size(x_min));
    while true
        x = sdpvar(n, t+1);         % State variable
        u = sdpvar(m, t);       % Control input
        u_tilde = sdpvar(m, t); % Adjusted control input
        y = sdpvar(p, t);         % Output variable
        x_hat = sdpvar(n, t+1);     % Estimated state
        r = sdpvar(p, t);       % Residual
        a_u = sdpvar(m, t);     % Control disturbance
        a_y = sdpvar(p, t);       % Output disturbance
        % Define constraints
        Constraints = [];
        
        % Initial state constraint
        Constraints = [Constraints, x(:,1) == x0, x_hat(:,1) == x0];
        
        % Dynamics and observer equations for all timesteps
        for i = 1:t
            % Control input and adjusted control input
            Constraints = [Constraints, u(:,i) == -K*x_hat(:,i), u_tilde(:,i) == u(:,i) + a_u(:,i)];
            
            % System dynamics
            Constraints = [Constraints, x(:,i+1) == A*x(:,i) + B*u_tilde(:,i)];
            Constraints = [Constraints, y(:,i) == C*x(:,i+1) + a_y(:,i)];
            
            % Observer dynamics
            Constraints = [Constraints, r(:,i) == y(:,i) - C*(A*x_hat(:,i) + B*u(:,i))];
            Constraints = [Constraints, x_hat(:,i+1) == A*x_hat(:,i) + B*u(:,i) + L*r(:,i)];
            
            % Error function threshold
            Constraints = [Constraints, norm(r(:,i)) <= Th];
            % Bound constraints
            Constraints = [Constraints, abs(y(:,i)) <= Y, abs(a_y(:,i)) <= Y];
            Constraints = [Constraints, abs(u(:,i)) <= U, abs(u_tilde(:,i)) <= U, abs(a_u(:,i)) <= U];
            Constraints = [Constraints, x_min <= x(:,i), x(:,i) <= x_max];
        end
        
        % Final state constraint
        M=[1000;1000];
        b=binvar(1);
        Constraints=[Constraints,x(:,t+1)>=x_max+0.0001-M*(1-b),x(:,t+1)<=x_min-0.0001+M*(b)];
        % Solver settings using Gurobi
        options = sdpsettings('solver','gurobi','verbose',0);
        Objective=0;
        % Solve the problem
        sol = optimize(Constraints, Objective, options);
        
        % Check for solver status
        if sol.problem == 0
            if mod(sam,10) == 0
                disp(sam)
            end
            dataset(1,1:t,sam)=value(a_u);
            dataset(2,1:t,sam)=value(a_y);
            dataset(:,15,sam)=t;
            dataset(:,16,sam)=x0;
            %disp(value(x));
            break;
        else
            t=t+1;
            if(t>12)
                break
            end
        end
    end
end