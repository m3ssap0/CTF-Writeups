.class LMainActivity$1;
.super Ljava/lang/Object;
.source "MainActivity.java"

# interfaces
.implements Landroid/view/View$OnClickListener;


# annotations
.annotation system Ldalvik/annotation/EnclosingMethod;
value = LMainActivity;->onCreate(Landroid/os/Bundle;)V
.end annotation

.annotation system Ldalvik/annotation/InnerClass;
accessFlags = 0x0
name = null
.end annotation


# instance fields
.field final synthetic this$0:LMainActivity;


# direct methods
.method constructor <init>(LMainActivity;)V
.registers 2

.line 63
iput-object p1, p0, LMainActivity$1;->this$0:LMainActivity;

invoke-direct {p0}, Ljava/lang/Object;-><init>()V

return-void
.end method


# virtual methods
.method public onClick(Landroid/view/View;)V
.registers 4

.line 67
iget-object p1, p0, LMainActivity$1;->this$0:LMainActivity;

iget-object p1, p1, LMainActivity;->ed1:Landroid/widget/EditText;

invoke-virtual {p1}, Landroid/widget/EditText;->getText()Landroid/text/Editable;

move-result-object p1

invoke-virtual {p1}, Ljava/lang/Object;->toString()Ljava/lang/String;

move-result-object p1

.line 68
iget-object v0, p0, LMainActivity$1;->this$0:LMainActivity;

iget-object v0, v0, LMainActivity;->ed2:Landroid/widget/EditText;

invoke-virtual {v0}, Landroid/widget/EditText;->getText()Landroid/text/Editable;

move-result-object v0

invoke-virtual {v0}, Ljava/lang/Object;->toString()Ljava/lang/String;

move-result-object v0

.line 69
invoke-static {v0}, LMainActivity;->md5(Ljava/lang/String;)Ljava/lang/String;

move-result-object v0

.line 70
const-string v1, "m&m"

invoke-virtual {p1, v1}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

move-result p1

const/4 v1, 0x0

if-eqz p1, :cond_3f
	
	iget-object p1, p0, LMainActivity$1;->this$0:LMainActivity;

iget-object p1, p1, LMainActivity;->secret:Ljava/lang/String;

invoke-virtual {v0, p1}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

move-result p1

if-eqz p1, :cond_3f
	
	.line 71
	iget-object p1, p0, LMainActivity$1;->this$0:LMainActivity;

invoke-virtual {p1}, LMainActivity;->getApplicationContext()Landroid/content/Context;

move-result-object p1

const-string v0, "Redirecting..."

invoke-static {p1, v0, v1}, Landroid/widget/Toast;->makeText(Landroid/content/Context;Ljava/lang/CharSequence;I)Landroid/widget/Toast;

move-result-object p1

.line 72
invoke-virtual {p1}, Landroid/widget/Toast;->show()V

goto :goto_82

.line 74
:cond_3f
iget-object p1, p0, LMainActivity$1;->this$0:LMainActivity;

invoke-virtual {p1}, LMainActivity;->getApplicationContext()Landroid/content/Context;

move-result-object p1

const-string v0, "Wrong Credentials"

invoke-static {p1, v0, v1}, Landroid/widget/Toast;->makeText(Landroid/content/Context;Ljava/lang/CharSequence;I)Landroid/widget/Toast;

move-result-object p1

invoke-virtual {p1}, Landroid/widget/Toast;->show()V

.line 76
iget-object p1, p0, LMainActivity$1;->this$0:LMainActivity;

iget-object p1, p1, LMainActivity;->tx1:Landroid/widget/TextView;

invoke-virtual {p1, v1}, Landroid/widget/TextView;->setVisibility(I)V

.line 77
iget-object p1, p0, LMainActivity$1;->this$0:LMainActivity;

iget-object p1, p1, LMainActivity;->tx1:Landroid/widget/TextView;

const/high16 v0, -0x10000

invoke-virtual {p1, v0}, Landroid/widget/TextView;->setBackgroundColor(I)V

.line 78
iget-object p1, p0, LMainActivity$1;->this$0:LMainActivity;

iget v0, p1, LMainActivity;->counter:I

add-int/lit8 v0, v0, -0x1

iput v0, p1, LMainActivity;->counter:I

.line 79
iget-object p1, p0, LMainActivity$1;->this$0:LMainActivity;

iget-object p1, p1, LMainActivity;->tx1:Landroid/widget/TextView;

iget-object v0, p0, LMainActivity$1;->this$0:LMainActivity;

iget v0, v0, LMainActivity;->counter:I

invoke-static {v0}, Ljava/lang/Integer;->toString(I)Ljava/lang/String;

move-result-object v0

invoke-virtual {p1, v0}, Landroid/widget/TextView;->setText(Ljava/lang/CharSequence;)V

.line 81
iget-object p1, p0, LMainActivity$1;->this$0:LMainActivity;

iget p1, p1, LMainActivity;->counter:I

if-nez p1, :cond_82
	
	.line 82
	iget-object p1, p0, LMainActivity$1;->this$0:LMainActivity;

iget-object p1, p1, LMainActivity;->b1:Landroid/widget/Button;

invoke-virtual {p1, v1}, Landroid/widget/Button;->setEnabled(Z)V

.line 85
:cond_82
:goto_82
return-void
.end method
