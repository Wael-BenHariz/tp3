import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

import { AppComponent } from './app.component';
import { AccueilComponent } from './composants/accueil/accueil.component';
import { ListmaterielComponent } from './composants/informatique/listmateriel/listmateriel.component';
import { MaterielComponent } from './composants/informatique/materiel/materiel.component';


@NgModule({
  declarations: [
    AppComponent,
    AccueilComponent,
    ListmaterielComponent,
    MaterielComponent
  ],
  imports: [
    BrowserModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
