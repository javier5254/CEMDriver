import { bootstrapApplication } from '@angular/platform-browser';
import { RouteReuseStrategy, provideRouter, withComponentInputBinding } from '@angular/router';
import { provideHttpClient, withInterceptors } from '@angular/common/http';
import { provideIonicAngular, IonicRouteStrategy } from '@ionic/angular';

import { AppComponent } from './app/app.component';
import { routes } from './app/app.routes';
import { authInterceptor } from './app/core/interceptors/auth.interceptor';
import { registerIcons } from './app/core/icons';

registerIcons();

// Nota: este stack (Ionic ^9 + Angular 22) asume una app zoneless por diseno
// (ver comentarios en @ionic/angular/dist/common/providers/angular-delegate.js).
// La deteccion de cambios automatica no siempre se re-dispara tras trabajo
// asincrono (HTTP, setInterval, geolocation.watchPosition), asi que cada
// componente que muta estado dentro de un callback async llama explicitamente
// a ChangeDetectorRef.detectChanges() (patron estandar zoneless) en vez de
// depender de un tick global implicito.
bootstrapApplication(AppComponent, {
  providers: [
    { provide: RouteReuseStrategy, useClass: IonicRouteStrategy },
    // mode: 'ios' fuerza los componentes de Ionic a renderizarse con su
    // variante estilo iOS (headers, botones, transiciones, switches) en vez
    // de Material Design, como parte del rediseno visual "mas Apple".
    provideIonicAngular({ mode: 'ios' }),
    provideRouter(routes, withComponentInputBinding()),
    provideHttpClient(withInterceptors([authInterceptor])),
  ],
}).catch((err) => console.error(err));
