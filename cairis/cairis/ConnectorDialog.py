#  Licensed to the Apache Software Foundation (ASF) under one
#  or more contributor license agreements.  See the NOTICE file
#  distributed with this work for additional information
#  regarding copyright ownership.  The ASF licenses this file
#  to you under the Apache License, Version 2.0 (the
#  "License"); you may not use this file except in compliance
#  with the License.  You may obtain a copy of the License at
#
#  http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing,
#  software distributed under the License is distributed on an
#  "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
#  KIND, either express or implied.  See the License for the
#  specific language governing permissions and limitations
#  under the License.


import wx
import armid
import WidgetFactory
from Borg import Borg

class ConnectorDialog(wx.Dialog):
  def __init__(self,parent,conName = '',fromComponent = '',fromInterface = '',toComponent = '',toInterface ='',assetName='',pName = '',arName = ''):
    wx.Dialog.__init__(self,parent,armid.PATTERNSTRUCTURE_ID,'Add Structure',style=wx.DEFAULT_DIALOG_STYLE|wx.MAXIMIZE_BOX|wx.THICK_FRAME,size=(400,350))
    b = Borg()
    self.dbProxy = b.dbProxy
    self.theConnectorName = conName
    self.theFromComponent = fromComponent
    self.theFromInterface = fromInterface
    self.theToComponent = toComponent
    self.theToInterface = toInterface
    self.theAssetName = assetName
    self.theProtocolName = pName
    self.theAccessRight = arName
    mainSizer = wx.BoxSizer(wx.VERTICAL)
    assets = self.dbProxy.getDimensionNames('template_asset')
    components = self.dbProxy.getDimensionNames('component')
    interfaces = self.dbProxy.getDimensionNames('interface')
    protocols = self.dbProxy.getDimensionNames('protocol')
    accessRights = self.dbProxy.getDimensionNames('access_right')
    mainSizer.Add(WidgetFactory.buildTextSizer(self,'Name',(87,30),armid.CONNECTOR_TEXTNAME_ID),0,wx.EXPAND)

    fromSizer = wx.BoxSizer(wx.HORIZONTAL)
    mainSizer.Add(fromSizer,0,wx.EXPAND)
    fromSizer.Add(WidgetFactory.buildComboSizerList(self,'From',(87,30),armid.CONNECTOR_COMBOFROMNAME_ID,components),1,wx.EXPAND)
    fromSizer.Add(WidgetFactory.buildComboSizerList(self,'Interface',(87,30),armid.CONNECTOR_COMBOFROMINTERFACE_ID,interfaces),1,wx.EXPAND)

    toSizer = wx.BoxSizer(wx.HORIZONTAL)
    mainSizer.Add(toSizer,0,wx.EXPAND)
    toSizer.Add(WidgetFactory.buildComboSizerList(self,'To',(87,30),armid.CONNECTOR_COMBOTONAME_ID,components),1,wx.EXPAND)
    toSizer.Add(WidgetFactory.buildComboSizerList(self,'Interface',(87,30),armid.CONNECTOR_COMBOTOINTERFACE_ID,interfaces),1,wx.EXPAND)
    mainSizer.Add(WidgetFactory.buildComboSizerList(self,'Asset',(87,30),armid.CONNECTOR_COMBOASSET_ID,assets),0,wx.EXPAND)
    metricsSizer = wx.BoxSizer(wx.HORIZONTAL)
    mainSizer.Add(metricsSizer,0,wx.EXPAND)
    metricsSizer.Add(WidgetFactory.buildComboSizerList(self,'Protocol',(87,30),armid.CONNECTOR_COMBOPROTOCOL_ID,protocols),1,wx.EXPAND)
    metricsSizer.Add(WidgetFactory.buildComboSizerList(self,'Access Right',(87,30),armid.CONNECTOR_COMBOACCESSRIGHT_ID,accessRights),1,wx.EXPAND)
    mainSizer.Add(wx.StaticText(self,-1),1,wx.EXPAND)
    mainSizer.Add(WidgetFactory.buildAddCancelButtonSizer(self,armid.CONNECTOR_BUTTONCOMMIT_ID),0,wx.ALIGN_CENTER)
    self.SetSizer(mainSizer)

    wx.EVT_BUTTON(self,armid.CONNECTOR_BUTTONCOMMIT_ID,self.onCommit)
    self.commitLabel = 'Add'
    if (len(self.theConnectorName) > 0):
      self.commitLabel = 'Edit'
      self.SetLabel('Edit Connector')
      conNameCtrl = self.FindWindowById(armid.CONNECTOR_TEXTNAME_ID)
      fromNameCtrl = self.FindWindowById(armid.CONNECTOR_COMBOFROMNAME_ID)
      fromIfCtrl = self.FindWindowById(armid.CONNECTOR_COMBOFROMINTERFACE_ID)
      toNameCtrl = self.FindWindowById(armid.CONNECTOR_COMBOTONAME_ID)
      toIfCtrl = self.FindWindowById(armid.CONNECTOR_COMBOTOINTERFACE_ID)
      assetCtrl = self.FindWindowById(armid.CONNECTOR_COMBOASSET_ID)
      pCtrl = self.FindWindowById(armid.CONNECTOR_COMBOPROTOCOL_ID)
      arCtrl = self.FindWindowById(armid.CONNECTOR_COMBOACCESSRIGHT_ID)
      buttonCtrl = self.FindWindowById(armid.CONNECTOR_BUTTONCOMMIT_ID)

      conNameCtrl.SetValue(self.theConnectorName)
      fromNameCtrl.SetStringSelection(self.theFromComponent)
      fromIfCtrl.SetStringSelection(self.theFromInterface)
      toNameCtrl.SetStringSelection(self.theToComponent)
      toIfCtrl.SetStringSelection(self.theToInterface)
      assetCtrl.SetStringSelection(self.theAssetName)
      pCtrl.SetStringSelection(self.theProtocolName)
      arCtrl.SetStringSelection(self.theAccessRight)

      buttonCtrl.SetLabel('Edit')
      

  def onCommit(self,evt):
    conNameCtrl = self.FindWindowById(armid.CONNECTOR_TEXTNAME_ID)
    fromNameCtrl = self.FindWindowById(armid.CONNECTOR_COMBOFROMNAME_ID)
    fromIfCtrl = self.FindWindowById(armid.CONNECTOR_COMBOFROMINTERFACE_ID)
    toNameCtrl = self.FindWindowById(armid.CONNECTOR_COMBOTONAME_ID)
    toIfCtrl = self.FindWindowById(armid.CONNECTOR_COMBOTOINTERFACE_ID)
    assetCtrl = self.FindWindowById(armid.CONNECTOR_COMBOASSET_ID)
    pCtrl = self.FindWindowById(armid.CONNECTOR_COMBOPROTOCOL_ID)
    arCtrl = self.FindWindowById(armid.CONNECTOR_COMBOACCESSRIGHT_ID)

    self.theConnectorName = conNameCtrl.GetValue()
    self.theFromComponent = fromNameCtrl.GetValue()
    self.theFromInterface = fromIfCtrl.GetValue()
    self.theToComponent = toNameCtrl.GetValue()
    self.theToInterface = toIfCtrl.GetValue()
    self.theAssetName = assetCtrl.GetValue()
    self.theProtocolName = pCtrl.GetValue()
    self.theAccessRight = arCtrl.GetValue()

    if (len(self.theConnectorName) == 0):
      dlg = wx.MessageDialog(self,'Name cannot be empty',self.commitLabel + ' Connector',wx.OK)
      dlg.ShowModal()
      dlg.Destroy()
      return
    elif (len(self.theFromComponent) == 0):
      dlg = wx.MessageDialog(self,'No from component selected',self.commitLabel + ' Connector',wx.OK)
      dlg.ShowModal()
      dlg.Destroy()
      return
    elif (len(self.theFromInterface) == 0):
      dlg = wx.MessageDialog(self,'No from interface selected',self.commitLabel + ' Connector',wx.OK)
      dlg.ShowModal()
      dlg.Destroy()
      return
    elif (len(self.theToComponent) == 0):
      dlg = wx.MessageDialog(self,'No to component selected',self.commitLabel + ' Component',wx.OK)
      dlg.ShowModal()
      dlg.Destroy()
      return
    elif (len(self.theToInterface) == 0):
      dlg = wx.MessageDialog(self,'No to interface selected',self.commitLabel + ' Component',wx.OK)
      dlg.ShowModal()
      dlg.Destroy()
      return
    elif (len(self.theAssetName) == 0):
      dlg = wx.MessageDialog(self,'No asset selected',self.commitLabel + ' Component',wx.OK)
      dlg.ShowModal()
      dlg.Destroy()
      return
    elif (len(self.theProtocolName) == 0):
      dlg = wx.MessageDialog(self,'No protocol selected',self.commitLabel + ' Component',wx.OK)
      dlg.ShowModal()
      dlg.Destroy()
      return
    elif (len(self.theAccessRight) == 0):
      dlg = wx.MessageDialog(self,'No access right selected',self.commitLabel + ' Component',wx.OK)
      dlg.ShowModal()
      dlg.Destroy()
      return
    else:
      self.EndModal(armid.CONNECTOR_BUTTONCOMMIT_ID)

  def name(self): return self.theConnectorName
  def fromComponent(self): return self.theFromComponent
  def fromInterface(self): return self.theFromInterface
  def toComponent(self): return self.theToComponent
  def toInterface(self): return self.theToInterface
  def protocol(self): return self.theProtocolName
  def accessRight(self): return self.theAccessRight
  def asset(self): return self.theAssetName