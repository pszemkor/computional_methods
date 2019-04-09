function y = newton(x0, f, df, epsilon, max_iter, prec)
%szybsza i zbiezna kwadratowo
%wady: moze sie rozbiec, trzeba znaæ pochodn¹

    digits(prec);
    x(1) = x0;
    x(2) = x(1) - f(x(1))/df(x(1));
    iter = 2;
    while (iter < max_iter) && (abs(x(iter) - x(iter-1)) > epsilon)
        iter = iter + 1;
        x(iter) = x(iter-1) - (f(x(iter-1))/df(x(iter-1)));
    end
    y = x(iter);
    disp(iter);
    disp(vpa(y));
end