import { IonicModule } from '@ionic/angular';
import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { RegisterComponent  } from './register.component';
import { ExploreContainerComponentModule } from '../explore-container/explore-container.module';
import { RegisterRoutingModule } from './register-routing.module';
import { IonicSelectableComponent } from 'ionic-selectable';


@NgModule({
  imports: [
    IonicModule,
    CommonModule,
    FormsModule,
    ExploreContainerComponentModule,
    ReactiveFormsModule,
    RegisterRoutingModule,
    IonicSelectableComponent
  ],
  declarations: [RegisterComponent ],
  exports: [RegisterComponent],
})
export class RegisterComponentModule {}