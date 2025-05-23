from rest_framework import serializers

class StockHistoryResponseBodyoutput1Serializer(serializers.Serializer):
    prdy_vrss = serializers.CharField(required=False)
    prdy_vrss_sign = serializers.CharField(required=False)
    prdy_ctrt = serializers.CharField(required=False)
    stck_prdy_clpr = serializers.CharField(required=False)
    acml_vol = serializers.CharField(required=False)
    acml_tr_pbmn = serializers.CharField(required=False)
    hts_kor_isnm = serializers.CharField(required=False)
    stck_prpr = serializers.CharField(required=False)
    stck_shrn_iscd = serializers.CharField(required=False)
    prdy_vol = serializers.CharField(required=False)
    stck_mxpr = serializers.CharField(required=False)
    stck_llam = serializers.CharField(required=False)
    stck_oprc = serializers.CharField(required=False)
    stck_hgpr = serializers.CharField(required=False)
    stck_lwpr = serializers.CharField(required=False)
    stck_prdy_oprc = serializers.CharField(required=False)
    stck_prdy_hgpr = serializers.CharField(required=False)
    stck_prdy_lwpr = serializers.CharField(required=False)
    askp = serializers.CharField(required=False)
    bidp = serializers.CharField(required=False)
    prdy_vrss_vol = serializers.CharField(required=False)
    vol_tnrt = serializers.CharField(required=False)
    stck_fcam = serializers.CharField(required=False)
    lstn_stcn = serializers.CharField(required=False)
    cpfn = serializers.CharField(required=False)
    hts_avls = serializers.CharField(required=False)
    per = serializers.CharField(required=False)
    eps = serializers.CharField(required=False)
    pbr = serializers.CharField(required=False)
    itewhol_loan_rmnd_ratem = serializers.CharField(required=False)

class StockHistoryResponseBodyoutput2Serializer(serializers.Serializer):
    stck_bsop_date = serializers.CharField(required=False)
    stck_clpr = serializers.CharField(required=False)
    stck_oprc = serializers.CharField(required=False)
    stck_hgpr = serializers.CharField(required=False)
    stck_lwpr = serializers.CharField(required=False)
    acml_vol = serializers.CharField(required=False)
    acml_tr_pbmn = serializers.CharField(required=False)
    flng_cls_code = serializers.CharField(required=False)
    prtt_rate = serializers.CharField(required=False)
    mod_yn = serializers.CharField(required=False)
    prdy_vrss_sign = serializers.CharField(required=False)
    prdy_vrss = serializers.CharField(required=False)
    revl_issu_reas = serializers.CharField(required=False)

class StockHistoryResponseBodySerializer(serializers.Serializer):
    rt_cd = serializers.CharField(required=False)
    msg_cd = serializers.CharField(required=False)
    msg1 = serializers.CharField(required=False)
    output1 = StockHistoryResponseBodyoutput1Serializer(required=False)
    output2 = StockHistoryResponseBodyoutput2Serializer(many=True, required=False)
