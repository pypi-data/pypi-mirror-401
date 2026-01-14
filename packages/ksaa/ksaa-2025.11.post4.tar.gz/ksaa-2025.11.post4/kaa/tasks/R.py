
from kaa.common import sprite_path
from kotonebot.backend.core import Image, HintBox, HintPoint



class Common:
    
    ButtonClose = Image(path=sprite_path(r"94a4392e-9464-4b4b-8bdb-1bb599ecd02b.png"), name="button_close.png")

    ButtonCompletion = Image(path=sprite_path(r"2c6d56a6-6b18-459e-b953-9fcff97c9351.png"), name="button_completion.png")

    ButtonConfirm = Image(path=sprite_path(r"b2fce55d-5afe-436f-9a8a-e39144fbc68f.png"), name="button_confirm.png")

    ButtonConfirmNoIcon = Image(path=sprite_path(r"78e339b8-5cfa-410b-8016-6f533c558df1.png"), name="button_confirm_no_icon.png")

    ButtonContest = Image(path=sprite_path(r"9c49e5d0-8a65-48b9-8e6f-6f469e1c837e.png"), name="button_contest.png")

    ButtonEnd = Image(path=sprite_path(r"12ed3509-5bdf-470d-8a4b-f7c0cb1f4bf3.png"), name="button_end.png")

    ButtonHome = Image(path=sprite_path(r"91b19419-7b65-4e0a-ad39-7ee485ee1053.png"), name="button_home.png")

    ButtonIconArrowShort = Image(path=sprite_path(r"7fa651f9-4926-4786-a9ff-6970b1d82c75.png"), name="button_icon_arrow_short.png")

    ButtonIconArrowShortDisabled = Image(path=sprite_path(r"0ebc1b46-abcc-45c4-b894-1ce2e43883c4.png"), name="button_icon_arrow_short_disabled.png")

    ButtonIconCheckMark = Image(path=sprite_path(r"77a3d9f6-e6d7-4007-8f9a-5351308802aa.png"), name="button_icon_check_mark.png")

    ButtonIconClose = Image(path=sprite_path(r"75b56861-8bd4-486d-833f-4decbd2da2c8.png"), name="button_icon_close.png")

    ButtonIdol = Image(path=sprite_path(r"5d45d8d9-3cdf-4d41-a1a1-1e65350e2f6b.png"), name="button_idol.png")

    ButtonIdolSupportCard = Image(path=sprite_path(r"8d000fdb-4c79-4041-805c-632762f603d0.png"), name="button_idol_support_card.png")

    ButtonNext = Image(path=sprite_path(r"18b5962f-aac7-483c-9345-bbff63589e4d.png"), name="button_next.png")

    ButtonNextNoIcon = Image(path=sprite_path(r"75388bcd-bf78-4284-810b-325fc1316577.png"), name="button_next_no_icon.png")

    ButtonRetry = Image(path=sprite_path(r"c775174c-32c4-49b5-94d1-a05a462ee902.png"), name="button_retry.png")

    ButtonSelect = Image(path=sprite_path(r"0a084595-639c-4458-8949-21ae7298c729.png"), name="button_select.png")

    ButtonStart = Image(path=sprite_path(r"60ca4ab0-7265-45d9-845c-a0d071bcc663.png"), name="button_start.png")

    ButtonToolbarMenu = Image(path=sprite_path(r"6bb429dd-a594-481d-974e-c3be0bc169b4.png"), name="button_toolbar_menu.png")

    CheckboxUnchecked = Image(path=sprite_path(r"8e5dac8d-3031-467f-aa82-5f1b93850fd3.png"), name="checkbox_unchecked.png")

    ShopPackButton = Image(path=sprite_path(r"5c49d3b3-656e-4c8c-ae1a-9b0209b9dcc3.png"), name="商店礼包页面按钮")

    ShopPackRedDot = HintBox(x1=650, y1=660, x2=687, y2=697, source_resolution=(720, 1280))

    ButtonToolbarHome = Image(path=sprite_path(r"7b5c8883-a1f9-4ce9-bd84-26668577dfc6.png"), name="工具栏的主页按钮")

    ButtonToolbarBack = Image(path=sprite_path(r"41904062-e218-4b28-972a-b5cfcd058d2c.png"), name="工具栏的返回按钮")

    TextGameUpdate = Image(path=sprite_path(r"9fe11a75-3f41-495e-9815-75914e1423a6.png"), name="text_game_update.png")

    TextNetworkError = Image(path=sprite_path(r"86b71a32-47dc-4fa7-935a-04f1ea236b41.png"), name="text_network_error.png")

    TextFastforwardCommuDialogTitle = Image(path=sprite_path(r"50e23c8a-7ba2-4c9c-9cfb-196c260fa1d5.png"), name="早送り確認")

    ButtonCommuSkip = Image(path=sprite_path(r"f1f21925-3e22-4dd1-b53b-bb52bcf26c2b.png"), name="跳过交流按钮")

    ButtonCommuFastforward = Image(path=sprite_path(r"f6ca6bd3-543f-4779-8367-c5c883f04b95.png"), name="快进交流按钮")

    ButtonOK = Image(path=sprite_path(r"8424ecdd-8857-4764-9fd0-d4bfa440c128.png"), name="OK 按钮")

    ButtonSelect2 = Image(path=sprite_path(r"5ebcde3b-f0fd-4e5d-b3de-ada8f0b5e03b.png"), name="選択する")

    TextSkipCommuComfirmation = Image(path=sprite_path(r"4d78add6-1027-4939-bb51-f99fca7db2ce.png"), name="跳过未读交流确认对话框标题")

    IconButtonCheck = Image(path=sprite_path(r"fad5eec2-5fd5-412f-9abb-987a3087dc54.png"), name="按钮✓图标")

    IconButtonCross = Image(path=sprite_path(r"bc7155ac-18c9-4335-9ec2-c8762d37a057.png"), name="按钮×图标")


    pass
class Daily:
    
    ButonLinkData = Image(path=sprite_path(r"3fe0f302-d01d-43cf-9737-43196b431e8f.png"), name="buton_link_data.png")

    ButtonAssignmentPartial = Image(path=sprite_path(r"6c9f9505-ab39-469d-913d-da9801427893.png"), name="button_assignment_partial.png")

    ButtonClaimAllNoIcon = Image(path=sprite_path(r"e4374676-07d2-4861-a184-2a302ab2183a.png"), name="button_claim_all_no_icon.png")

    ButtonClubCollectReward = Image(path=sprite_path(r"ae4060d9-f94d-4e47-8132-80c948823a78.png"), name="button_club_collect_reward.png")

    ButtonClubSendGift = Image(path=sprite_path(r"042e1fc1-8e7f-4051-8834-67bb3e55c7e4.png"), name="button_club_send_gift.png")

    ButtonClubSendGiftNext = Image(path=sprite_path(r"fcf6b0ea-9008-4dda-aa71-53763e851f9a.png"), name="button_club_send_gift_next.png")

    ButtonContestChallenge = Image(path=sprite_path(r"f67ffbd2-9315-4a24-880b-793a3b84fafb.png"), name="button_contest_challenge.png")

    ButtonContestChallengeStart = Image(path=sprite_path(r"3a6ddfea-0957-4dd5-a735-dc6eed70f9a6.png"), name="button_contest_challenge_start.png")

    ButtonContestRanking = Image(path=sprite_path(r"1de18cd8-603e-496a-ac3a-5e771e970898.png"), name="button_contest_ranking.png")

    ButtonContestStart = Image(path=sprite_path(r"d2150580-1d0e-4151-9256-ad76e04b806c.png"), name="button_contest_start.png")

    ButtonDailyShop = Image(path=sprite_path(r"503430f7-42d0-4f7d-a719-afe20390af36.png"), name="button_daily_shop.png")

    ButtonHomeCurrent = Image(path=sprite_path(r"4b8826fd-dde6-4f11-afca-b24074e36b21.png"), name="button_home_current.png")

    ButtonIconPass = Image(path=sprite_path(r"4815a7bc-20f1-4d38-bafa-c68a8da246ec.png"), name="button_icon_pass.png")

    ButtonIconSkip = Image(path=sprite_path(r"b6f3db58-d735-4092-9783-e9f2aed25347.png"), name="button_icon_skip.png")

    ButtonMission = Image(path=sprite_path(r"baf790e3-78bb-4d85-961c-705656059058.png"), name="button_mission.png")

    ButtonPass = Image(path=sprite_path(r"8de2d45e-be71-4432-8778-d585e9d2f993.png"), name="button_pass.png")

    ButtonPassClaim = Image(path=sprite_path(r"7b6f55ab-417d-426e-ba4d-2a270a679f8a.png"), name="button_pass_claim.png")

    ButtonPresentsPartial = Image(path=sprite_path(r"7c9b078a-dcf4-437e-9b43-bcc28e3a64a9.png"), name="button_presents_partial.png")

    ButtonProduce = Image(path=sprite_path(r"236d4e29-d957-442d-909b-32fed2caf866.png"), name="button_produce.png")

    ButtonShop = Image(path=sprite_path(r"769c9e28-9710-448e-b7d1-baed09088bb6.png"), name="button_shop.png")

    ButtonShopCapsuleToys = Image(path=sprite_path(r"b6508d2f-b607-4ae7-b3be-869f05894b81.png"), name="button_shop_capsule_toys.png")

    ButtonShopCapsuleToysDraw = Image(path=sprite_path(r"ef5fa19d-68ad-4e7a-b041-59d9c1aa502c.png"), name="button_shop_capsule_toys_draw.png")

    ButtonShopCountAdd = Image(path=sprite_path(r"9a0b9710-a4f1-4619-809e-098e019e286d.png"), name="button_shop_count_add.png")

    ButtonShopCountAddDisabled = Image(path=sprite_path(r"51f383ca-cf74-4315-8605-efe3ff9771f2.png"), name="button_shop_count_add_disabled.png")

    ButtonSupportCardUpgrade = Image(path=sprite_path(r"c678c607-dfc7-4fa6-9bd3-e6304a519c42.png"), name="button_support_card_upgrade.png")

    ButtonRefreshMoneyShop = Image(path=sprite_path(r"81c97cd3-df53-44d3-bf3d-1eb4dc67b62a.png"), name="リスト更新：1回無料")

    IconTitleDailyShop = Image(path=sprite_path(r"e9ee330d-dfca-440e-8b8c-0a3b4e8c8730.png"), name="日常商店标题图标")

    BoxHomeAssignment = HintBox(x1=33, y1=650, x2=107, y2=746, source_resolution=(720, 1280))

    BoxHomeAP = HintBox(x1=291, y1=4, x2=500, y2=82, source_resolution=(720, 1280))

    BoxHomeJewel = HintBox(x1=500, y1=7, x2=703, y2=82, source_resolution=(720, 1280))

    BoxHomeActivelyFunds = HintBox(x1=29, y1=530, x2=109, y2=633, source_resolution=(720, 1280))

    IconAssignKouchou = Image(path=sprite_path(r"71e39ed1-8bb1-4a29-959a-84a60bc7019e.png"), name="icon_assign_kouchou.png")

    IconAssignMiniLive = Image(path=sprite_path(r"95ec6780-deb1-45d1-beae-8cde5b76b918.png"), name="icon_assign_mini_live.png")

    IconAssignOnlineLive = Image(path=sprite_path(r"915cec33-f922-48d5-b366-c63d01b72013.png"), name="icon_assign_online_live.png")

    IconAssignTitle = Image(path=sprite_path(r"32498029-75e2-461a-84c2-790cc349c6c6.png"), name="icon_assign_title.png")

    IconMenuClub = Image(path=sprite_path(r"e77bce9a-a887-462b-ac78-1f412d55e78f.png"), name="icon_menu_club.png")

    IconShopAp = Image(path=sprite_path(r"ed384e5c-da4b-4611-a8a4-307d26390826.png"), name="icon_shop_ap.png")

    IconShopMoney = Image(path=sprite_path(r"d60d860b-6fc5-4a20-8869-a592bbad32cb.png"), name="icon_shop_money.png")

    IconShopTitle = Image(path=sprite_path(r"6762c0ee-d1a7-4f16-a628-186e7ffc8300.png"), name="icon_shop_title.png")

    IconTitleAssign = Image(path=sprite_path(r"2d626511-e4ac-49f0-977a-8cbc5fe2247c.png"), name="icon_title_assign.png")

    IconTitlePass = Image(path=sprite_path(r"df8e934a-7d6b-4784-bc18-271398e5ddfc.png"), name="icon_title_pass.png")

    BoxApkUpdateDialogTitle = HintBox(x1=26, y1=905, x2=342, y2=967, source_resolution=(720, 1280))

    ButtonAssignmentShortenTime = Image(path=sprite_path(r"1652f06a-5417-49ef-8949-4854772d9ab7.png"), name="工作页面 短缩 时间")

    class Club:
        
        NoteRequestHintBox = HintBox(x1=314, y1=1071, x2=450, y2=1099, source_resolution=(720, 1280))
    
    
        pass
    TextRoadToIdol = Image(path=sprite_path(r"4503db6b-7224-4b81-9971-e7cfa56e10f2.png"), name="文字「アイドルへの道」")

    PointContest = HintPoint(x=492, y=878)

    PointDissmissContestReward = HintPoint(x=604, y=178)

    TextDateChangeDialogConfirmButton = Image(path=sprite_path(r"eaad330d-4e50-4b55-be2c-8da0f72764d9.png"), name="日期变更对话框的确认按钮")

    TextDateChangeDialog = Image(path=sprite_path(r"9483fae5-3a72-4684-9403-d25d2c602d3d.png"), name="日期变更对话框")

    BoxMissonTabs = HintBox(x1=11, y1=929, x2=703, y2=1030, source_resolution=(720, 1280))

    class CapsuleToys:
        
        NextPageStartPoint = HintPoint(x=360, y=1167)
    
        NextPageEndPoint = HintPoint(x=362, y=267)
    
        IconTitle = Image(path=sprite_path(r"2bd6fe88-99fa-443d-8e42-bb3de5881213.png"), name="日常 扭蛋 页面标题图标")
    
        SliderStartPoint = HintPoint(x=476, y=898)
    
        SliderEndPoint = HintPoint(x=230, y=898)
    
    
        pass
    TextDefaultExchangeCountChangeDialog = Image(path=sprite_path(r"de325534-3fd3-480a-9eb8-eb47960a753a.png"), name="商店默认购买次数改变对话框")

    TextShopItemPurchased = Image(path=sprite_path(r"5d36b880-7b3f-49b1-a018-7de59867d376.png"), name="交換しました")

    TextShopItemSoldOut = Image(path=sprite_path(r"24dc7158-036c-4a66-9280-e934f470be53.png"), name="交換済みです")

    class SupportCard:
        
        DragDownStartPoint = HintPoint(x=357, y=872)
    
        DragDownEndPoint = HintPoint(x=362, y=194)
    
        TargetSupportCard = HintPoint(x=138, y=432)
    
    
        pass
    WeeklyFreePack = Image(path=sprite_path(r"ae4742aa-acda-442d-bf73-b3fe7b66e85c.png"), name="每周免费礼包购买按钮")

    TextActivityFundsMax = Image(path=sprite_path(r"839999db-973e-49f6-b6b0-9352d35dc6d2.png"), name="text_activity_funds_max.png")

    TextAssignmentCompleted = Image(path=sprite_path(r"22cdeaa5-1e93-43ea-a85c-92b20dc059dc.png"), name="text_assignment_completed.png")

    TextContest = Image(path=sprite_path(r"41d4b221-c456-489e-ae1a-10c4de604a2f.png"), name="text_contest.png")

    TextContestLastOngoing = Image(path=sprite_path(r"6cb70525-e991-49f5-a5b3-28307a91bb77.png"), name="text_contest_last_ongoing.png")

    TextContestNoMemory = Image(path=sprite_path(r"095b8d2c-bee8-425e-b95a-bd08c85dd4d0.png"), name="text_contest_no_memory.png")

    TextContestOverallStats = Image(path=sprite_path(r"9b1985c1-918d-4639-8493-55eed1c777c2.png"), name="text_contest_overall_stats.png")

    TextShopRecommended = Image(path=sprite_path(r"4699465d-f69c-4f48-8acb-b7600f5ad85b.png"), name="text_shop_recommended.png")

    TextTabShopAp = Image(path=sprite_path(r"57667ce4-83b4-43d2-af6e-8458c5e61c03.png"), name="text_tab_shop_ap.png")


    pass
class Shop:
    
    ItemLessonNote = Image(path=sprite_path(r"0949c622-9067-4f0d-bac2-3f938a1d2ed2.png"), name="レッスンノート")

    ItemVeteranNote = Image(path=sprite_path(r"b2af59e9-60e3-4d97-8c72-c7ba092113a3.png"), name="ベテランノート")

    ItemSupportEnhancementPt = Image(path=sprite_path(r"835489e2-b29b-426c-b4c9-3bb9f8eb6195.png"), name="サポート強化Pt 支援强化Pt")

    ItemSenseNoteVocal = Image(path=sprite_path(r"c5b7d67e-7260-4f08-a0e9-4d31ce9bbecf.png"), name="センスノート（ボーカル）感性笔记（声乐）")

    ItemSenseNoteDance = Image(path=sprite_path(r"0f7d581d-cea3-4039-9205-732e4cd29293.png"), name="センスノート（ダンス）感性笔记（舞蹈）")

    ItemSenseNoteVisual = Image(path=sprite_path(r"d3cc3323-51af-4882-ae12-49e7384b746d.png"), name="センスノート（ビジュアル）感性笔记（形象）")

    ItemLogicNoteVocal = Image(path=sprite_path(r"a1df3af1-a3e7-4521-a085-e4dc3cd1cc57.png"), name="ロジックノート（ボーカル）理性笔记（声乐）")

    ItemLogicNoteDance = Image(path=sprite_path(r"a9fcaf04-0c1f-4b0f-bb5b-ede9da96180f.png"), name="ロジックノート（ダンス）理性笔记（舞蹈）")

    ItemLogicNoteVisual = Image(path=sprite_path(r"c3f536d6-a04a-4651-b3f9-dd2c22593f7f.png"), name="ロジックノート（ビジュアル）理性笔记（形象）")

    ItemAnomalyNoteVocal = Image(path=sprite_path(r"eef25cf9-afd0-43b1-b9c5-fbd997bd5fe0.png"), name="アノマリーノート（ボーカル）非凡笔记（声乐）")

    ItemAnomalyNoteDance = Image(path=sprite_path(r"df991b42-ed8e-4f2c-bf0c-aa7522f147b6.png"), name="アノマリーノート（ダンス）非凡笔记（舞蹈）")

    ItemAnomalyNoteVisual = Image(path=sprite_path(r"9340b854-025c-40da-9387-385d38433bef.png"), name="アノマリーノート（ビジュアル）非凡笔记（形象）")

    ItemRechallengeTicket = Image(path=sprite_path(r"ea1ba124-9cb3-4427-969a-bacd47e7d920.png"), name="再挑戦チケット 重新挑战券")

    ItemRecordKey = Image(path=sprite_path(r"1926f2f9-4bd7-48eb-9eba-28ec4efb0606.png"), name="記録の鍵  解锁交流的物品")

    class IdolPiece:
        
        花海咲季_FightingMyWay = Image(path=sprite_path(r"3942ae40-7f22-412c-aebe-4b064f68db9b.png"), name="")
    
        月村手毬_LunaSayMaybe = Image(path=sprite_path(r"185f7838-92a7-460b-9340-f60858948ce9.png"), name="")
    
        藤田ことね_世界一可愛い私  = Image(path=sprite_path(r"cb3d0ca7-8d14-408a-a2f5-2e25f7b86d6c.png"), name="")
    
        花海佑芽_TheRollingRiceball = Image(path=sprite_path(r"213016c2-c3a2-43d8-86a3-ab4d27666ced.png"), name="")
    
        葛城リーリヤ_白線 = Image(path=sprite_path(r"cc60b509-2ed5-493d-bb9f-333c6d2a6006.png"), name="")
    
        紫云清夏_TameLieOneStep = Image(path=sprite_path(r"5031808b-5525-4118-92b4-317ec8bda985.png"), name="")
    
        篠泽广_光景 = Image(path=sprite_path(r"ae9fe233-9acc-4e96-ba8e-1fb1d9bc2ea5.png"), name="")
    
        倉本千奈_WonderScale = Image(path=sprite_path(r"8f8b7b46-53bb-42ab-907a-4ea87eb09ab4.png"), name="")
    
        有村麻央_Fluorite = Image(path=sprite_path(r"0d9ac648-eefa-4869-ac99-1b0c83649681.png"), name="")
    
        姬崎莉波_clumsy_trick = Image(path=sprite_path(r"921eefeb-730e-46fc-9924-d338fb286592.png"), name="")
    
    
        pass

    pass
class Produce:
    
    BoxProduceOngoing = HintBox(x1=179, y1=937, x2=551, y2=1091, source_resolution=(720, 1280))

    ButtonAutoSet = Image(path=sprite_path(r"1124789b-e1ae-4a85-8a05-84c442ba8195.png"), name="button_auto_set.png")

    ButtonProduce = Image(path=sprite_path(r"b7116495-97ab-4978-8cc3-ef9efc216c7d.png"), name="button_produce.png")

    ButtonProduceStart = Image(path=sprite_path(r"5f2dd097-da4c-45ad-a181-07f66e4233c4.png"), name="button_produce_start.png")

    ButtonRegular = Image(path=sprite_path(r"e4593451-b636-4112-ac0f-f6915e6af32a.png"), name="button_regular.png")

    CheckboxIconNoteBoost = Image(path=sprite_path(r"72f38668-3412-4a53-b19f-f8cdb9badc11.png"), name="checkbox_icon_note_boost.png")

    CheckboxIconSupportPtBoost = Image(path=sprite_path(r"313a2168-ce6c-4d10-9d83-520435cd9dae.png"), name="checkbox_icon_support_pt_boost.png")

    IconPIdolLevel = Image(path=sprite_path(r"30a6f399-6999-4f04-bb77-651e0214112f.png"), name="P偶像卡上的等级图标")

    KbIdolOverviewName = HintBox(x1=140, y1=16, x2=615, y2=97, source_resolution=(720, 1280))

    BoxIdolOverviewIdols = HintBox(x1=26, y1=568, x2=696, y2=992, source_resolution=(720, 1280))

    ButtonResume = Image(path=sprite_path(r"ccbcb114-7f73-43d1-904a-3a7ae660c531.png"), name="再開する")

    ResumeDialogRegular = Image(path=sprite_path(r"daf3d823-b7f1-4584-acf3-90b9d880332c.png"), name="培育再开对话框 REGULAR")

    BoxResumeDialogWeeks = HintBox(x1=504, y1=559, x2=643, y2=595, source_resolution=(720, 1280))

    BoxResumeDialogIdolCard = HintBox(x1=53, y1=857, x2=197, y2=1048, source_resolution=(720, 1280))

    ResumeDialogPro = Image(path=sprite_path(r"c954e153-d3e9-4488-869f-d00cfdfac5ee.png"), name="培育再开对话框 PRO")

    ResumeDialogMaster = Image(path=sprite_path(r"3c8b477a-8eda-407e-9e9f-7540c8808f89.png"), name="培育再开对话框 MASTER")

    BoxResumeDialogWeeks_Saving = HintBox(x1=499, y1=377, x2=638, y2=413, source_resolution=(720, 1280))

    BoxResumeDialogIdolCard_Saving = HintBox(x1=54, y1=674, x2=197, y2=867, source_resolution=(720, 1280))

    RadioTextSkipCommu = Image(path=sprite_path(r"647ffc7b-b40a-4b56-9723-b6b58d094882.png"), name="radio_text_skip_commu.png")

    TextAnotherIdolAvailableDialog = Image(path=sprite_path(r"cbf4ce9c-f8d8-4fb7-a197-15bb9847df04.png"), name="Another 版本偶像可用对话框标题")

    SwitchEventModeOff = Image(path=sprite_path(r"c5356ad6-0f1e-42be-b090-059f33ea7cee.png"), name="イベントモード 切换开关 OFF")

    SwitchEventModeOn = Image(path=sprite_path(r"44097699-487f-4932-846a-095a427f4ed8.png"), name="イベントモード 切换开关 ON")

    ScreenshotMemoryConfirmDialog = Image(path=sprite_path(r"eb0f0e5a-f480-4a7f-a111-ad1c0c76e36a.png"), name="screenshot_memory_confirm_dialog.png")

    LogoNia = Image(path=sprite_path(r"a0bd6a5f-784d-4f0a-9d66-10f4b80c8d3e.png"), name="NIA LOGO (NEXT IDOL AUDITION)")

    PointNiaToHajime = HintPoint(x=34, y=596)

    TextAPInsufficient = Image(path=sprite_path(r"4883c564-f950-4a29-9f5f-6f924123cd22.png"), name="培育 AP 不足提示弹窗 标题")

    ButtonRefillAP = Image(path=sprite_path(r"eaba6ebe-f0df-4918-aee5-ef4e3ffedcf0.png"), name="确认恢复AP按钮")

    ButtonUse = Image(path=sprite_path(r"cfc9c8e8-cbe1-49f0-9afa-ead7f9455a2e.png"), name="按钮「使う」")

    ScreenshotNoEnoughAp3 = Image(path=sprite_path(r"1a2a7cc7-da19-4be6-836b-dc8232c52563.png"), name="screenshot_no_enough_ap_3.png")

    ButtonSkipLive = Image(path=sprite_path(r"e5e84f9e-28da-4cf4-bcba-c9145fe39b07.png"), name="培育结束跳过演出按钮")

    TextSkipLiveDialogTitle = Image(path=sprite_path(r"b6b94f21-ef4b-4425-9c7e-ca2b574b0add.png"), name="跳过演出确认对话框标题")

    ButtonHajime0Regular = Image(path=sprite_path(r"6cd80be8-c9b3-4ba5-bf17-3ffc9b000743.png"), name="")

    ButtonHajime0Pro = Image(path=sprite_path(r"55f7db71-0a18-4b3d-b847-57959b8d2e32.png"), name="")

    TitleIconProudce = Image(path=sprite_path(r"0bf5e34e-afc6-4447-bbac-67026ce2ad26.png"), name="培育页面左上角标题图标")

    ButtonHajime1Regular = Image(path=sprite_path(r"3b473fe6-e147-477f-b088-9b8fb042a4f6.png"), name="")

    ButtonHajime1Pro = Image(path=sprite_path(r"2ededcf5-1d80-4e2a-9c83-2a31998331ce.png"), name="")

    ButtonHajime1Master = Image(path=sprite_path(r"24e99232-9434-457f-a9a0-69dd7ecf675f.png"), name="")

    PointHajimeToNia = HintPoint(x=680, y=592)

    LogoHajime = Image(path=sprite_path(r"e6b45405-cd9f-4c6e-a9f1-6ec953747c65.png"), name="Hajime LOGO 定期公演")

    ButtonPIdolOverview = Image(path=sprite_path(r"e88c9ad1-ec37-4fcd-b086-862e1e7ce8fd.png"), name="Pアイドルー覧  P偶像列表展示")

    TextStepIndicator1 = Image(path=sprite_path(r"44ba8515-4a60-42c9-8878-b42e4e34ee15.png"), name="1. アイドル選択")

    BoxSelectedIdol = HintBox(x1=149, y1=783, x2=317, y2=1006, source_resolution=(720, 1280))

    BoxSetCountIndicator = HintBox(x1=66, y1=651, x2=139, y2=686, source_resolution=(720, 1280))

    PointProduceNextSet = HintPoint(x=702, y=832)

    PointProducePrevSet = HintPoint(x=14, y=832)

    TextStepIndicator2 = Image(path=sprite_path(r"a48324ae-7c1a-489e-b3c4-93d12267f88d.png"), name="2. サポート選択")

    EmptySupportCardSlot = Image(path=sprite_path(r"d3424d31-0502-4623-996e-f0194e5085ce.png"), name="空支援卡槽位")

    TextAutoSet = Image(path=sprite_path(r"f5c16d2f-ebc5-4617-9b96-971696af7c52.png"), name="おまかせ編成")

    TextStepIndicator3 = Image(path=sprite_path(r"f43c313b-8a7b-467b-8442-fc5bcb8b4388.png"), name="3.メモリー選択")

    TextRentAvailable = Image(path=sprite_path(r"74ec3510-583d-4a76-ac69-38480fbf1387.png"), name="レンタル可能")

    TextStepIndicator4 = Image(path=sprite_path(r"b62bf889-da3c-495a-8707-f3bde73efe92.png"), name="4.開始確認")


    pass
class InPurodyuusu:
    
    A = Image(path=sprite_path(r"a89e2ea7-4fb6-496d-a660-b97531aa3363.png"), name="A.png")

    AcquireBtnDisabled = Image(path=sprite_path(r"33482100-a9e3-4614-87c6-f95f54f64f91.png"), name="acquire_btn_disabled.png")

    ButtonCancel = Image(path=sprite_path(r"3c626e31-daed-427d-b268-33f00d37a57e.png"), name="button_cancel.png")

    ButtonComplete = Image(path=sprite_path(r"aa609ed0-8c5e-40ff-8af3-922be0c8425a.png"), name="button_complete.png")

    ButtonFinalPracticeDance = Image(path=sprite_path(r"cd4f98a5-1ef2-4cee-9303-042ad1f9b215.png"), name="button_final_practice_dance.png")

    ButtonFinalPracticeVisual = Image(path=sprite_path(r"ffa19928-3a91-4f33-9939-678977980277.png"), name="button_final_practice_visual.png")

    ButtonFinalPracticeVocal = Image(path=sprite_path(r"c01abde7-e706-47f2-8667-4be64ac23dcb.png"), name="button_final_practice_vocal.png")

    ButtonFollowNoIcon = Image(path=sprite_path(r"28227141-5f28-49ff-8ae0-473c494729d7.png"), name="button_follow_no_icon.png")

    ButtonIconStudy = Image(path=sprite_path(r"2ae6a0b6-613d-438a-b4c4-5aff4faf3bd8.png"), name="button_icon_study.png")

    ButtonIconStudyVisual = Image(path=sprite_path(r"c3e50e49-e63d-4791-81b8-899d8b3c952a.png"), name="button_icon_study_visual.png")

    ButtonLeave = Image(path=sprite_path(r"7afa246c-e22a-4ce7-8845-9d016f8bbc1e.png"), name="button_leave.png")

    ButtonNextNoIcon = Image(path=sprite_path(r"2d175abe-ff7d-4e5b-a6b9-6400a58e997b.png"), name="button_next_no_icon.png")

    ButtonRetry = Image(path=sprite_path(r"441c87e8-5cbb-47b5-9038-e24007ca58e7.png"), name="button_retry.png")

    ButtonTextActionOuting = Image(path=sprite_path(r"2f6259cc-0e8b-4f26-9681-131984d203a7.png"), name="button_text_action_outing.png")

    ButtonTextAllowance = Image(path=sprite_path(r"a03f906d-42cd-47ee-a017-4a234efaab16.png"), name="button_text_allowance.png")

    ButtonTextConsult = Image(path=sprite_path(r"99a58d2b-d1a2-446f-a9a8-f68b020084e6.png"), name="button_text_consult.png")

    IconClearBlue = Image(path=sprite_path(r"461bd433-34d0-4938-b6bd-54c4d9ef0943.png"), name="icon_clear_blue.png")

    IconTitleAllowance = Image(path=sprite_path(r"4831c563-deda-4979-a8cf-e1075f80056a.png"), name="icon_title_allowance.png")

    IconTitleStudy = Image(path=sprite_path(r"755ea096-27cd-4086-b83e-81bf39dab971.png"), name="icon_title_study.png")

    LootboxSliverLock = Image(path=sprite_path(r"e39c6ab1-25e7-4f18-9acb-a93c2cc762fc.png"), name="lootbox_sliver_lock.png")

    LootBoxSkillCard = Image(path=sprite_path(r"8f547414-61f5-4d64-8c78-ebf365b81de8.png"), name="loot_box_skill_card.png")

    M = Image(path=sprite_path(r"828bfd19-4936-4a68-a534-fb935b89d974.png"), name="M.png")

    BoxExamTop = HintBox(x1=5, y1=2, x2=712, y2=55, source_resolution=(720, 1280))

    BoxCardLetter = HintBox(x1=6, y1=1081, x2=715, y2=1100, source_resolution=(720, 1280))

    BoxDrink = HintBox(x1=39, y1=1150, x2=328, y2=1244, source_resolution=(720, 1280))

    BoxDrink1 = HintBox(x1=53, y1=1166, x2=121, y2=1234, source_resolution=(720, 1280))

    BoxDrink2 = HintBox(x1=149, y1=1166, x2=217, y2=1234, source_resolution=(720, 1280))

    BoxDrink3 = HintBox(x1=245, y1=1166, x2=313, y2=1234, source_resolution=(720, 1280))

    PDrinkIcon = Image(path=sprite_path(r"118db7f0-32dc-4963-b013-d2e0208e3502.png"), name="p_drink_icon.png")

    PItemIconColorful = Image(path=sprite_path(r"861d5de7-91f9-468a-b182-70cae9394845.png"), name="p_item_icon_colorful.png")

    PSkillCardIconBlue = Image(path=sprite_path(r"bfbab95d-55f5-4c0c-b9e7-f802d5e229c2.png"), name="p_skill_card_icon_blue.png")

    PSkillCardIconColorful = Image(path=sprite_path(r"ef9d4c16-90ef-472e-a4ab-67698926b2d3.png"), name="p_skill_card_icon_colorful.png")

    Rest = Image(path=sprite_path(r"29aed432-d20b-4e26-9d73-a5790b04eaeb.png"), name="rest.png")

    RestConfirmBtn = Image(path=sprite_path(r"db90551e-4975-4404-ab7b-1b35b69e1406.png"), name="rest_confirm_btn.png")

    Screenshot1Cards = Image(path=sprite_path(r"a92a9188-b3ee-4367-bfbb-11d6379945fc.png"), name="screenshot_1_cards.png")

    Screenshot4Cards = Image(path=sprite_path(r"a5f9565c-17af-443f-8cbe-c6304181ac10.png"), name="screenshot_4_cards.png")

    Screenshot5Cards = Image(path=sprite_path(r"95a83d44-c8df-4efe-8b7b-15c8cda50269.png"), name="screenshot_5_cards.png")

    BoxWeeksUntilExam = HintBox(x1=11, y1=8, x2=237, y2=196, source_resolution=(720, 1280))

    TextActionVocal = Image(path=sprite_path(r"d6b64759-26b7-45b1-bf8e-5c0d98611e0d.png"), name="Vo. レッスン")

    TextActionDance = Image(path=sprite_path(r"303cccc1-c674-4d3a-8c89-19ea729fdbef.png"), name="Da. レッスン")

    TextActionVisual = Image(path=sprite_path(r"cc8a495d-330d-447d-8a80-a8a6ecc409c5.png"), name="Vi. レッスン")

    IconAsariSenseiAvatar = Image(path=sprite_path(r"d7667903-7149-4f2f-9c15-d8a4b5f4d347.png"), name="Asari 老师头像")

    BoxAsariSenseiTip = HintBox(x1=245, y1=150, x2=702, y2=243, source_resolution=(720, 1280))

    ButtonPracticeVocal = Image(path=sprite_path(r"ce1d1d6f-38f2-48bf-98bd-6e091c7ca5b8.png"), name="行动页 声乐课程按钮图标")

    ButtonPracticeDance = Image(path=sprite_path(r"b2e1bf3c-2c36-4fb5-9db7-c10a29563a37.png"), name="行动页 舞蹈课程按钮图标")

    ButtonPracticeVisual = Image(path=sprite_path(r"adc533a7-970b-4c5b-a037-2181531a35d6.png"), name="行动页 形象课程按钮图标")

    TextFinalExamRemaining = Image(path=sprite_path(r"70898bf8-56c5-4f84-becb-629c9ab6a7da.png"), name="最終まで")

    ButtonIconOuting = Image(path=sprite_path(r"8ded6c98-85ea-4858-a66d-4fc8caecb7c5.png"), name="行动按钮图标 外出（おでかけ）")

    ButtonIconConsult = Image(path=sprite_path(r"d83f338d-dde3-494b-9bea-cae511e3517c.png"), name="行动按钮图标 咨询（相談）")

    TextMidExamRemaining = Image(path=sprite_path(r"ce20a856-5629-4f8e-a8e1-d1bd14e18e4f.png"), name="中間まで")

    IconTitleConsult = Image(path=sprite_path(r"23d88465-65d9-4718-8725-8dbf0a98a5a4.png"), name="「相談」页面左上角图标")

    PointConsultFirstItem = HintPoint(x=123, y=550)

    ButtonEndConsult = Image(path=sprite_path(r"9fd0753f-c607-4d49-82d1-40bda27e014f.png"), name="相談 结束按钮")

    ButtonIconExchange = Image(path=sprite_path(r"4096cffa-a889-4622-852e-760fc7022d93.png"), name="交换按钮的图标")

    TextExchangeConfirm = Image(path=sprite_path(r"25f00ee3-8dfe-42d1-a67e-191fa5c3df4b.png"), name="交換確認")

    ScreenshotDrinkTest = Image(path=sprite_path(r"645187dd-4327-4b3f-88bd-80c17c80adb9.png"), name="screenshot_drink_test.png")

    ScreenshotDrinkTest3 = Image(path=sprite_path(r"7c415841-221e-43dc-8c4c-6776e84dcc07.png"), name="screenshot_drink_test_3.png")

    TextRechallengeEndProduce = Image(path=sprite_path(r"207594fa-6a0b-45ec-aeff-b3e45348c508.png"), name="再挑战对话框的结束培育")

    TextGoalClearNext = Image(path=sprite_path(r"05890a1b-8764-4e9f-9d21-65d292c22e13.png"), name="培育目标达成 NEXT 文字")

    BoxLessonCards5_1 = HintBox(x1=16, y1=882, x2=208, y2=1136, source_resolution=(720, 1280))

    BoxNoSkillCard = HintBox(x1=180, y1=977, x2=529, y2=1026, source_resolution=(720, 1280))

    TitleIconOuting = Image(path=sprite_path(r"ee4e512b-4982-49b6-9c71-31984b58e1d0.png"), name="外出（おでかけ）页面 标题图标")

    TextPDrinkMaxConfirmTitle = Image(path=sprite_path(r"582d36c0-0916-4706-9833-4fbc026701f5.png"), name="P饮料溢出 不领取弹窗标题")

    ButtonUse = Image(path=sprite_path(r"a3736105-b3e6-467b-888a-f93b8f4d37be.png"), name="使用按钮（使用饮料按钮）")

    IconTitleSkillCardRemoval = Image(path=sprite_path(r"bab6c393-692c-4681-ac0d-76c0d9dabea6.png"), name="技能卡自选删除 标题图标")

    ButtonRemove = Image(path=sprite_path(r"00551158-fee9-483f-b034-549139a96f58.png"), name="削除")

    TextPDrink = Image(path=sprite_path(r"8c179a21-be6f-4db8-a9b0-9afeb5c36b1c.png"), name="文本「Pドリンク」")

    TextDontClaim = Image(path=sprite_path(r"e4683def-8d1d-472b-a5ab-bb3885c0c98e.png"), name="受け取らない")

    ButtonDontClaim = Image(path=sprite_path(r"447d0e44-5d87-4b7c-8e60-edb111fe1639.png"), name="「受け取らない」按钮")

    BoxSelectPStuffComfirm = HintBox(x1=256, y1=1064, x2=478, y2=1128, source_resolution=(720, 1280))

    TextClaim = Image(path=sprite_path(r"c948f136-416f-447e-8152-54a1cd1d1329.png"), name="文字「受け取る」")

    TextPItem = Image(path=sprite_path(r"0c0627be-4a09-4450-a078-1858d3ace532.png"), name="文字「Pアイテム」")

    TextSkillCard = Image(path=sprite_path(r"d271a24f-efe8-424d-8fd5-f6b3756ba4ca.png"), name="文字「スキルカード」")

    TextRecommend = Image(path=sprite_path(r"b0283997-7931-476d-a92f-d7569f6ea34c.png"), name="おすすめ")

    ScreenshotSenseiTipConsult = Image(path=sprite_path(r"6ba64b62-758a-4771-a24e-94d95fb8f932.png"), name="screenshot_sensei_tip_consult.png")

    TextSkillCardSelectGuideDialogTitle = Image(path=sprite_path(r"3f637e86-6b74-4693-9131-1fe411fc21e5.png"), name="獲得ガイド表示設定")

    BoxSkillCardAcquired = HintBox(x1=194, y1=712, x2=528, y2=765, source_resolution=(720, 1280))

    IconSkillCardEventBubble = Image(path=sprite_path(r"6b58d90d-2e5e-4b7f-bc01-941f2633de89.png"), name="技能卡事件气泡框图标")

    ScreenshotSkillCardEnhanceDialog = Image(path=sprite_path(r"735994f3-533b-459e-bddc-db466ad3e89b.png"), name="screenshot_skill_card_enhance_dialog.png")

    IconTitleSkillCardEnhance = Image(path=sprite_path(r"79abd239-5eed-4195-9fa8-d729daa874ca.png"), name="技能卡强化 标题 图标")

    ButtonEnhance = Image(path=sprite_path(r"da439e8c-3b74-4371-9657-0736d826c7d1.png"), name="技能卡 强化按钮")

    IconTitleSkillCardMove = Image(path=sprite_path(r"db7d3f03-1f7f-43bf-8125-f7c2d345fca2.png"), name="培育中技能卡移动对话框")

    BoxSkillCardMoveButtonCount = HintBox(x1=339, y1=1170, x2=381, y2=1195, source_resolution=(720, 1280))

    T = Image(path=sprite_path(r"16fbc93d-b294-4001-b4e9-ee2af181415f.png"), name="睡意卡字母 T（眠気）")

    IconSp = Image(path=sprite_path(r"d982d2b5-4bc0-4ae9-a516-f29c2848d64b.png"), name="SP 课程图标")

    BoxCommuEventButtonsArea = HintBox(x1=14, y1=412, x2=703, y2=1089, source_resolution=(720, 1280))

    TextSelfStudyVocal = Image(path=sprite_path(r"c78c38cc-7b61-4dc4-820d-0a5b684ef52e.png"), name="文化课事件 自习 声乐")

    TextSelfStudyDance = Image(path=sprite_path(r"83d0a033-466c-463a-bb8c-be0f2953e9b2.png"), name="文化课事件 自习 舞蹈")

    TextSelfStudyVisual = Image(path=sprite_path(r"4695f96b-c4f5-4bb6-a021-a13b6ceb2883.png"), name="文化课事件 自习 形象")

    TextAsariProduceEnd = Image(path=sprite_path(r"03213eb8-de56-42ff-826e-c3bab6761778.png"), name="text_asari_produce_end.png")

    TextButtonExamSkipTurn = Image(path=sprite_path(r"3351e66f-43d8-4d12-88ec-ba2553cdd788.png"), name="text_button_exam_skip_turn.png")

    TextClearUntil = Image(path=sprite_path(r"710cfaf7-a4b5-4c8a-a3a0-a54e9e062941.png"), name="text_clear_until.png")

    TextDance = Image(path=sprite_path(r"f945b9e7-1e71-4b4a-8f0c-3286ed0c6c60.png"), name="text_dance.png")

    TextFinalProduceRating = Image(path=sprite_path(r"cdadb205-ef60-4978-8def-d5ade238bc98.png"), name="text_final_produce_rating.png")

    TextOneWeekRemaining = Image(path=sprite_path(r"02bdd34f-4979-4adf-9381-9c994fb14bc9.png"), name="text_one_week_remaining.png")

    TextPerfectUntil = Image(path=sprite_path(r"6020f0fb-41bb-4c6e-8b28-5c8fdacb3703.png"), name="text_perfect_until.png")

    TextPleaseSelectPDrink = Image(path=sprite_path(r"89b50dea-7e7e-4f85-aa20-d4f4c12e67cc.png"), name="text_please_select_p_drink.png")

    TextPDiary = Image(path=sprite_path(r"7b5f4a02-d556-4ac3-b912-f635b31bf166.png"), name="text_p_diary.png")

    TextPDrinkMax = Image(path=sprite_path(r"dffde4a9-f203-4af2-94d0-b154486290f1.png"), name="text_p_drink_max.png")

    TextSenseiTipConsult = Image(path=sprite_path(r"5ce9f211-bdc0-4508-a170-ee5998b484e1.png"), name="text_sensei_tip_consult.png")

    TextSenseiTipDance = Image(path=sprite_path(r"2f8310f2-4004-413a-bf76-cad98865b677.png"), name="text_sensei_tip_dance.png")

    TextSenseiTipRest = Image(path=sprite_path(r"7264af1b-75fa-4d41-bad7-939dd5de1261.png"), name="text_sensei_tip_rest.png")

    TextSenseiTipVisual = Image(path=sprite_path(r"e8cc3f86-72bb-4713-b0c7-e3f19ecfbfbe.png"), name="text_sensei_tip_visual.png")

    TextSenseiTipVocal = Image(path=sprite_path(r"2bf85eb5-270b-47dc-a7c9-ad038f307451.png"), name="text_sensei_tip_vocal.png")

    TextSkipTurnDialog = Image(path=sprite_path(r"1ad467ce-3d4b-4131-901b-c983c6153d9e.png"), name="text_skip_turn_dialog.png")

    TextVisual = Image(path=sprite_path(r"1949db37-8a3b-4c67-b7d7-87b959e83f51.png"), name="text_visual.png")


    pass
class Kuyo:
    
    ButtonStartGame = Image(path=sprite_path(r"3ad1cc3f-2152-4803-b19b-21694657103e.png"), name="button_start_game.png")

    ButtonTab3Speedup = Image(path=sprite_path(r"a589bef5-f3cd-4184-a7a8-7f0d0347b0be.png"), name="button_tab3_speedup.png")


    pass