import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';

import { IonicModule } from '@ionic/angular';

import { ReadByIdPageRoutingModule } from './read-by-id-routing.module';

import { ReadByIdPage } from './read-by-id.page';
import { IonicSelectableComponent } from 'ionic-selectable';

@NgModule({
  imports: [
    CommonModule,
    FormsModule,
    IonicModule,
    ReadByIdPageRoutingModule,
    ReactiveFormsModule,
    IonicSelectableComponent
  ],
  declarations: [ReadByIdPage]
})
export class ReadByIdPageModule {}
