function res = bisection(prec,a,b,epsilon,fun)
%fajna, bo zawsze zbiega do jakiegoœ miejsca zerowego
%zaklada, ze jest roznica znakow na krancach przedzialow
    if(sign(fun(a) * fun(b)) > 0)
        error("wrong a and b");
    end
    iter = 0;
    digits(prec);
    while abs(a-b) >= epsilon 
        iter = iter + 1;
        mid = (a + b) / 2;
        
        if abs(fun(mid)) <= epsilon
            break;
        elseif fun(mid) * fun(a) < 0
            b = mid;
        else
            a = mid;
        end
    end
    disp("iteracje: ");
    disp(iter);
    res = mid;
    disp(vpa(res));
end
