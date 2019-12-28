.class public LMainActivity;
.super Landroid/app/Activity;
.source "MainActivity.java"


# instance fields
.field b1:Landroid/widget/Button;

.field b2:Landroid/widget/Button;

.field counter:I

.field ed1:Landroid/widget/EditText;

.field ed2:Landroid/widget/EditText;

.field lol:Ljava/util/List;
    .annotation system Ldalvik/annotation/Signature;
        value = {
            "Ljava/util/List<",
            "Ljava/lang/String;",
            ">;"
        }
    .end annotation
.end field

.field magic:Ljava/lang/String;

.field secret:Ljava/lang/String;

.field tx1:Landroid/widget/TextView;


# direct methods
.method public constructor <init>()V
    .registers 5

    .line 14
    invoke-direct {p0}, Landroid/app/Activity;-><init>()V

    .line 19
    const/4 v0, 0x3

    iput v0, p0, LMainActivity;->counter:I

    .line 21
    const/16 v1, 0x8

    new-array v1, v1, [Ljava/lang/String;

    const-string v2, "84"

    const/4 v3, 0x0

    aput-object v2, v1, v3

    const-string v2, "5"

    const/4 v3, 0x1

    aput-object v2, v1, v3

    const-string v2, "2"

    const/4 v3, 0x2

    aput-object v2, v1, v3

    const-string v2, "f8eb53473"

    aput-object v2, v1, v0

    const-string v0, "4"

    const/4 v2, 0x4

    aput-object v0, v1, v2

    const-string v0, "2efb3d"

    const/4 v2, 0x5

    aput-object v0, v1, v2

    const-string v0, "f"

    const/4 v2, 0x6

    aput-object v0, v1, v2

    const-string v0, "82df"

    const/4 v2, 0x7

    aput-object v0, v1, v2

    invoke-static {v1}, Ljava/util/Arrays;->asList([Ljava/lang/Object;)Ljava/util/List;

    move-result-object v0

    iput-object v0, p0, LMainActivity;->lol:Ljava/util/List;

    .line 22
    const-string v0, "a"

    iget-object v1, p0, LMainActivity;->lol:Ljava/util/List;

    invoke-static {v0, v1}, Ljava/lang/String;->join(Ljava/lang/CharSequence;Ljava/lang/Iterable;)Ljava/lang/String;

    move-result-object v0

    iput-object v0, p0, LMainActivity;->magic:Ljava/lang/String;

    .line 23
    iget-object v0, p0, LMainActivity;->magic:Ljava/lang/String;

    const-string v1, "8"

    const-string v2, "0"

    invoke-virtual {v0, v1, v2}, Ljava/lang/String;->replaceAll(Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;

    move-result-object v0

    iput-object v0, p0, LMainActivity;->secret:Ljava/lang/String;

    return-void
.end method

.method public static final md5(Ljava/lang/String;)Ljava/lang/String;
    .registers 6

    .line 29
    :try_start_0
    const-string v0, "MD5"

    .line 30
    invoke-static {v0}, Ljava/security/MessageDigest;->getInstance(Ljava/lang/String;)Ljava/security/MessageDigest;

    move-result-object v0

    .line 31
    invoke-virtual {p0}, Ljava/lang/String;->getBytes()[B

    move-result-object p0

    invoke-virtual {v0, p0}, Ljava/security/MessageDigest;->update([B)V

    .line 32
    invoke-virtual {v0}, Ljava/security/MessageDigest;->digest()[B

    move-result-object p0

    .line 35
    new-instance v0, Ljava/lang/StringBuffer;

    invoke-direct {v0}, Ljava/lang/StringBuffer;-><init>()V

    .line 36
    const/4 v1, 0x0

    :goto_17
    array-length v2, p0

    if-ge v1, v2, :cond_41

    .line 37
    aget-byte v2, p0, v1

    and-int/lit16 v2, v2, 0xff

    invoke-static {v2}, Ljava/lang/Integer;->toHexString(I)Ljava/lang/String;

    move-result-object v2

    .line 38
    :goto_22
    invoke-virtual {v2}, Ljava/lang/String;->length()I

    move-result v3

    const/4 v4, 0x2

    if-ge v3, v4, :cond_3b

    .line 39
    new-instance v3, Ljava/lang/StringBuilder;

    invoke-direct {v3}, Ljava/lang/StringBuilder;-><init>()V

    const-string v4, "0"

    invoke-virtual {v3, v4}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v3, v2}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v3}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v2

    goto :goto_22

    .line 40
    :cond_3b
    invoke-virtual {v0, v2}, Ljava/lang/StringBuffer;->append(Ljava/lang/String;)Ljava/lang/StringBuffer;

    .line 36
    add-int/lit8 v1, v1, 0x1

    goto :goto_17

    .line 42
    :cond_41
    invoke-virtual {v0}, Ljava/lang/StringBuffer;->toString()Ljava/lang/String;

    move-result-object p0
    :try_end_45
    .catch Ljava/security/NoSuchAlgorithmException; {:try_start_0 .. :try_end_45} :catch_46

    return-object p0

    .line 44
    :catch_46
    move-exception p0

    .line 45
    invoke-virtual {p0}, Ljava/security/NoSuchAlgorithmException;->printStackTrace()V

    .line 47
    const-string p0, ""

    return-object p0
.end method


# virtual methods
.method protected onCreate(Landroid/os/Bundle;)V
    .registers 3

    .line 52
    invoke-super {p0, p1}, Landroid/app/Activity;->onCreate(Landroid/os/Bundle;)V

    .line 53
    const p1, 0x7f030030

    invoke-virtual {p0, p1}, LMainActivity;->setContentView(I)V

    .line 55
    const p1, 0x7f030074

    invoke-virtual {p0, p1}, LMainActivity;->findViewById(I)Landroid/view/View;

    move-result-object p1

    check-cast p1, Landroid/widget/Button;

    iput-object p1, p0, LMainActivity;->b1:Landroid/widget/Button;

    .line 56
    const p1, 0x7f030075

    invoke-virtual {p0, p1}, LMainActivity;->findViewById(I)Landroid/view/View;

    move-result-object p1

    check-cast p1, Landroid/widget/EditText;

    iput-object p1, p0, LMainActivity;->ed1:Landroid/widget/EditText;

    .line 57
    const p1, 0x7f030076

    invoke-virtual {p0, p1}, LMainActivity;->findViewById(I)Landroid/view/View;

    move-result-object p1

    check-cast p1, Landroid/widget/EditText;

    iput-object p1, p0, LMainActivity;->ed2:Landroid/widget/EditText;

    .line 59
    const p1, 0x7f030077

    invoke-virtual {p0, p1}, LMainActivity;->findViewById(I)Landroid/view/View;

    move-result-object p1

    check-cast p1, Landroid/widget/Button;

    iput-object p1, p0, LMainActivity;->b2:Landroid/widget/Button;

    .line 60
    const p1, 0x7f030078

    invoke-virtual {p0, p1}, LMainActivity;->findViewById(I)Landroid/view/View;

    move-result-object p1

    check-cast p1, Landroid/widget/TextView;

    iput-object p1, p0, LMainActivity;->tx1:Landroid/widget/TextView;

    .line 61
    iget-object p1, p0, LMainActivity;->tx1:Landroid/widget/TextView;

    const/16 v0, 0x8

    invoke-virtual {p1, v0}, Landroid/widget/TextView;->setVisibility(I)V

    .line 63
    iget-object p1, p0, LMainActivity;->b1:Landroid/widget/Button;

    new-instance v0, LMainActivity$1;

    invoke-direct {v0, p0}, LMainActivity$1;-><init>(LMainActivity;)V

    invoke-virtual {p1, v0}, Landroid/widget/Button;->setOnClickListener(Landroid/view/View$OnClickListener;)V

    .line 88
    iget-object p1, p0, LMainActivity;->b2:Landroid/widget/Button;

    new-instance v0, LMainActivity$2;

    invoke-direct {v0, p0}, LMainActivity$2;-><init>(LMainActivity;)V

    invoke-virtual {p1, v0}, Landroid/widget/Button;->setOnClickListener(Landroid/view/View$OnClickListener;)V

    .line 94
    return-void
.end method

