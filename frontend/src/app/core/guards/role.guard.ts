import { inject } from '@angular/core';
import { CanActivateFn, Router } from '@angular/router';
import { AuthService } from '../services/auth.service';
import { Rol } from '../models';

export const roleGuard: CanActivateFn = (route) => {
  const auth = inject(AuthService);
  const router = inject(Router);
  const allowed = route.data?.['roles'] as Rol[] | undefined;

  const user = auth.getUser();
  if (!user) {
    return router.createUrlTree(['/login']);
  }

  if (!allowed || allowed.includes(user.rol)) {
    return true;
  }

  // Rol no autorizado para esta area: redirige a su propia area.
  return router.createUrlTree([auth.homeRouteForRole(user.rol)]);
};
