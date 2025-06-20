import { IonicModule } from '@ionic/angular';
import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { LoginComponent  } from './login.component';
import { ExploreContainerComponentModule } from '../explore-container/explore-container.module';
import { LoginRoutingModule } from './login-routing.module';
import { HttpClientModule } from '@angular/common/http';
import { RegisterComponentModule } from '../register/register.module';


@NgModule({
  imports: [
    IonicModule,
    CommonModule,
    FormsModule,
    ExploreContainerComponentModule,
    ReactiveFormsModule,
    LoginRoutingModule,
    HttpClientModule,
    RegisterComponentModule
  ],
  declarations: [LoginComponent],
  exports: [LoginComponent]
})
export class LoginComponentModule {}