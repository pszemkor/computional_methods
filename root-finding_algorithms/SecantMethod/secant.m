function y = secant(a, b,  f, epsilon, max_iter, prec)
%brak gwarancji zbieznosci
    if(sign(f(a) * f(b)) > 0)
        error("wrong a and b");
    end
    digits(prec);
    x(1) = a;
    x(2) = b;
    x(3) = x(2) - (f(x(2)) * ((x(2) - x(1))/ (f(x(2))- f(x(1)))));
    iter = 3;
    while (iter < max_iter) && (abs(x(iter) - x(iter-1)) > epsilon)
        iter = iter + 1;
        x(iter) = x(iter-1) - (f(x(iter-1)) * ((x(iter-1) - x(iter-2))/ (f(x(iter-1))- f(x(iter-2)))));
    end
    y = x(iter);
    disp(iter);
    disp(vpa(y));
end